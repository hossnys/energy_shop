config = require "lapis.config"

config "development", -> 
    port 8080

config "production", ->
    port 8
    num_workers 4
    code_cache "on"