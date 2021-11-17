import Widget from require "lapis.html"

class Firstform extends Widget
  content: =>
    @content_for "main", ->
      form method:"POST", action: @url_for("next"), ->
        div class:"form-group", ->
          label for:"coin_amount", ->
            text "I would like to swap (bitcoins)" --support drop menu later.

          input class:"form-control", type:"text", name:"coin_amount"

        div class:"form-group", ->
          label for:"tftcoin_amount", ->
            text "This gives you"
          i class:"fa fa-info-circle pull-right", ["data-toggle"]:"tooltip", ["data-placement"]:"top", title:"Calculated on bases of btc-alpha.com BTC/TFT tradingpair."
          
          input class:"form-control", type:"text", name:"tftcoin_amount"
            
        div class:"form-group", ->
          label for:"tftaddress", ->
            text "Your TFT Wallet Address"
          i class:"fa fa-info-circle pull-right", ["data-toggle"]:"tooltip", ["data-placement"]:"top", title:"Install the ThreeFold Foundation App (available on App Store & Google Play)"
          
          input class:"form-control", type:"text", name:"tftaddress"

        div class:"form-group", ->
          label for:"email", ->
            text "Your TFT Wallet Address"
          i class:"fa fa-info-circle pull-right", ["data-toggle"]:"tooltip", ["data-placement"]:"top", title:"We will only send you status updates regarding your transactions. No marketing ever."

          input class:"form-control", type:"email", name:"email" 

        div class:"form-group", -> 
          button class:"btn btn-primary", type:"submit", "Generate QR Code"
          
          
