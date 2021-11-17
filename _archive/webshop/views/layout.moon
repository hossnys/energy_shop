import Widget from require "lapis.html"


class SiteLayout extends Widget
  content: =>
    html_5 -> 
        head -> title @title or "TFT Webshop"
        body -> @content_for "main"