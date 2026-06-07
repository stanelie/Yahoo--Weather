
#
# This file is the default set of rules to compile a Pebble project.
#
# Feel free to customize this to your needs.
#

try:
    from sh import CommandNotFound, jshint, ErrorReturnCode_2
    hint = jshint
except (ImportError, CommandNotFound):
    hint = None

top = '.'
out = 'build'

def options(ctx):
    ctx.load('pebble_sdk')

def configure(ctx):
    ctx.load('pebble_sdk')
    ctx.env.BUNDLE_NAME = 'yweather2.pbw'
    global hint
    if hint is not None:
        hint = hint.bake(['--config', 'pebble-jshintrc'])

def build(ctx):
    if False and hint is not None:
        try:
            hint("src/js/pebble-js-app.js", _tty_out=False) # no tty because there are none in the cloudpebble sandbox.
        except ErrorReturnCode_2 as e:
            ctx.fatal("\nJavaScript linting failed (you can disable this in Project Settings):\n" + e.stdout)

    ctx.load('pebble_sdk')

    binaries = []

    cached_env = ctx.env
    for platform in ctx.env.TARGET_PLATFORMS:
        ctx.env = ctx.all_envs[platform]
        ctx.set_group(ctx.env.PLATFORM_NAME)
        app_elf = '{}/pebble-app.elf'.format(ctx.env.BUILD_DIR)
        ctx.pbl_build(source=ctx.path.ant_glob('src/**/*.c'),
                      target=app_elf,
                      bin_type='app')
        binaries.append({'platform': platform, 'app_elf': app_elf})
    ctx.env = cached_env

    ctx.set_group('bundle')
    ctx.pbl_bundle(binaries=binaries,
                   js=ctx.path.ant_glob('src/js/**/*.js'))
