
from flask_assets import Environment, Bundle


def compile_static_assets(app):
   
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
   
    account_less_bundle = Bundle(
        'src/less/account.less',
        filters='less,cssmin',
        output=f'dist/css/account.css',
        extra={'rel': 'stylesheet/less'}
    )
    dashboard_less_bundle = Bundle(
        'src/less/dashboard.less',
        filters='less,cssmin',
        output=f'dist/css/dashboard.css',
        extra={'rel': 'stylesheet/less'}
    )
    
    js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )
    
    assets.register('account_less_bundle', account_less_bundle)
    assets.register('dashboard_less_bundle', dashboard_less_bundle)
    assets.register('js_all', js_bundle)
   
    account_less_bundle.build()
    dashboard_less_bundle.build()
    js_bundle.build()
