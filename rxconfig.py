import reflex as rx

config = rx.Config(
    app_name="pyfilelib",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)