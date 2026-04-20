import reflex as rx

config = rx.Config(
    app_name="chauchaapp_banckend",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)