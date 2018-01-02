#include <cstring>
#include <vector>
#include <iostream>

#include "webgl.h"
#include "GetBufferSubDataWorker.h"

GetBufferSubDataWorker::GetBufferSubDataWorker(
    Nan::Callback *callback
  , v8::Local<v8::Object> contextRef
  , WebGLRenderingContext *context
  , GLenum target
  , GLint offset
  , v8::Local<v8::Value> arrayArg) :
      AsyncWorker(callback)
    , context(context)
    , target(target)
    , offset(offset) {

  self.Reset(contextRef);
  array.Reset(arrayArg);
  Nan::TypedArrayContents<char> dataArray(arrayArg);
  to = *dataArray;

  length = dataArray.length();

  context->glFlush();
  sync = context->glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);

  // Make sure context is no longer active
  context->clearActive();
}

void GetBufferSubDataWorker::Execute () {
  GLint64 timeout;

  eglMakeCurrent(context->DISPLAY, EGL_NO_SURFACE, EGL_NO_SURFACE, context->context);

  context->glGetInteger64v(GL_MAX_SERVER_WAIT_TIMEOUT, &timeout);
  context->glClientWaitSync(sync, GL_SYNC_FLUSH_COMMANDS_BIT, timeout);

  void *mappedBuf = context->glMapBufferRange(target, offset, length, GL_MAP_READ_BIT);
  memcpy(to, mappedBuf, length);

  context->glUnmapBuffer(target);
}

void GetBufferSubDataWorker::HandleOKCallback () {
  Nan::HandleScope scope;

  context->glDeleteSync(sync);

  array.Reset();
  self.Reset();

  v8::Local<v8::Value> argv[] = { Nan::Null() };
  callback->Call(1, argv);
}
