import Widget from require "lapis.html"

class Index extends Widget
  content: =>
    @content_for "main", ->
        h1 class: "header", "Hello"
        div class: "body", ->
            text "index page" 