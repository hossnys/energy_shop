lapis = require "lapis"

FirstForm = require("views.firstform")

class extends lapis.Application
  @enable "etlua"

  layout: "layout"

  [index: "/"]: =>
    -- @page_title: "TFT Webshop"
    render: "firstform"
  
  [next: "/next"]: =>
    print @params
    render: "firstform"