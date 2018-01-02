{
  'targets': [
    {
      'target_name': 'webgl',
      'defines': [
        'VERSION=1.0.0'
      ],
      'sources': [
          'src/bindings.cc',
          'src/webgl.cc',
          'src/procs.cc',
          'src/GetBufferSubDataWorker.cc'
      ],
      'include_dirs': [
        "<!(node -e \"require('nan')\")",
        '<(module_root_dir)/deps/include',
        "node_modules/angle/include"
      ],
      'library_dirs': [
        '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj'
      ],
      'dependencies': [
        'angle',
      ],
      'conditions': [
        ['OS=="mac"', {
            'libraries': [
                '-lANGLE',
                '-langle_common',
                '-langle_image_util',
                '-langle_gpu_info_util',
                '-ltranslator',
                '-lpreprocessor',
                '-lEGL_static',
                '-lGLESv2_static',
                '-framework QuartzCore',
                '-framework Quartz'
            ],
            'xcode_settings': {
                    'MACOSX_DEPLOYMENT_TARGET': '10.9'
            }
        }],
        ['OS=="linux"', {
            'libraries': [
                '-lANGLE',
                '-langle_common',
                '-langle_image_util',
                '-langle_gpu_info_util',
                '-ltranslator',
                '-lpreprocessor',
                '-lEGL_static',
                '-lGLESv2_static'
            ],
        }],
        ['OS=="win"', {
            'library_dirs': [
              '<(module_root_dir)/deps/windows/lib/<(target_arch)',
            ],
            'libraries': [
              'libEGL.lib',
              'libGLESv2.lib'
            ],
            'defines' : [
              'WIN32_LEAN_AND_MEAN',
              'VC_EXTRALEAN'
            ],
            'configurations': {
              'Release': {
                'msvs_settings': {
                  'VCCLCompilerTool': {
                    'RuntimeLibrary': 0, # static release
                    'Optimization': 0, # /Od, disabled
                    'FavorSizeOrSpeed': 1, # /Ot, favour speed over size
                    'InlineFunctionExpansion': 2, # /Ob2, inline anything eligible
                    'WholeProgramOptimization': 'false', # No
                    'OmitFramePointers': 'true',
                    'EnableFunctionLevelLinking': 'true',
                    'EnableIntrinsicFunctions': 'true',
                    'RuntimeTypeInfo': 'false',
                    'ExceptionHandling': '0',
                    'AdditionalOptions': [
                      '/MP', # compile across multiple CPUs
                    ]
                  },
                  'VCLinkerTool': {
                    'LinkTimeCodeGeneration': 0, # Link Time Code generation default
                    'OptimizeReferences': 1, # /OPT:NOREF
                    'EnableCOMDATFolding': 1, # /OPT:NOICF
                    'LinkIncremental': 2, # /INCREMENTAL
                  }
                },
                'msvs_configuration_attributes':
                {
                    'OutputDirectory': '$(SolutionDir)$(ConfigurationName)',
                    'IntermediateDirectory': '$(OutDir)\\obj\\$(ProjectName)'
                }
              }
            },
            "copies": [
              {
                'destination': '$(SolutionDir)$(ConfigurationName)',
                'files': [
                  '<(module_root_dir)/deps/windows/dll/<(target_arch)/libEGL.dll',
                  '<(module_root_dir)/deps/windows/dll/<(target_arch)/libGLESv2.dll'
                ]
              }
           ]
          }
        ]
      ]
    },
    {
      'target_name': 'angle',
      'actions': [
        {
        'action_name': 'build_angle',
        'inputs': [
          'scripts/build_angle.sh'
        ],
        'outputs': [
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libANGLE.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libangle_common.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libangle_image_util.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libangle_gpu_info_util.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libtranslator.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libpreprocessor.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libEGL_static.a',
          '<(module_root_dir)/node_modules/angle/out/$(BUILDTYPE)/obj/libGLESv2_static.a'
        ],
        'action': [ 'scripts/build_angle.sh', '$(BUILDTYPE)' ],
        }
      ]
    }
  ]
}
