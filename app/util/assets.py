from flask_assets import Environment, Bundle

bundles = {
    'home_css': Bundle(
        'style/scss/main.scss',
        filters='libsass',
        depends='styles/scss/*.scss',
        output='gen/home.%(version)s.css'
    )
}