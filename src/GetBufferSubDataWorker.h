class GetBufferSubDataWorker : public Nan::AsyncWorker {
 public:
  GetBufferSubDataWorker(
    Nan::Callback *callback,
    v8::Local<v8::Object> contextRef,
    WebGLRenderingContext *context,
    GLenum target,
    GLint offset,
    v8::Local<v8::Value> arrayArg);

  ~GetBufferSubDataWorker() {}

  void Execute ();

  void HandleOKCallback ();

 private:
  WebGLRenderingContext *context;
  GLsync sync;
  GLenum target;
  GLint offset;
  Nan::Persistent<v8::Object> self;
  Nan::Persistent<v8::Value> array;
  void *to;
  GLint length;
};
