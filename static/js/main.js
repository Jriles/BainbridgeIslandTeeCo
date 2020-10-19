var primary_color = "";

function setPrimaryColor(color_value){
    primary_color = color_value;
    console.log("primary_color: " + primary_color);
}

function submitNewTableOrder(table, row){
    console.log(table);
    console.log(row);
    console.log(table.rows);
}

$(function() {
  "use strict";
  //------- Parallax -------//
  skrollr.init({
    forceHeight: false
  });

  //------- Active Nice Select --------//
  //$('select').niceSelect();

   //want to expand images when we click on the expand button
  $('.expandImage').on('click', function(){
  //var nextCard = this.parentElement.parentElement.parentElement.parentElement.parentElement.nextSibling.children[0];
  var thisCard = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  console.log(this.parentElement.parentElement.parentElement.parentElement.parentElement.nextElementSibling);
  var nextCard = this.parentElement.parentElement.parentElement.parentElement.parentElement.nextElementSibling;
  var theImage = $(this).parent().parent().parent().first();
  var titleArea = thisCard.firstElementChild.children[1];
  console.log(titleArea);
  if(this.classList.contains("collapsed")){
    thisCard.style.zIndex = "100";
    $(theImage).animate({
        width: 500,
        height: 500
    }, 2000, function() {
        // Animation complete.
    });

    thisCard
    $(titleArea).animate({
        left: 100,
        position: relative
    }, 2000, function(){
        //animation complete
    });

    $(this).removeClass("collapsed");
    $(this).addClass( "expanded" );
  }else if(this.classList.contains("expanded")){
    $(this).addClass( "collapsed" );
    thisCard.style.zIndex = "10";
    $(this).removeClass("expanded");
    console.log("thinks it was expanded");
    $(theImage).animate({
        width: 254,
        height: 275
    }, 2000, function() {
        // Animation complete.
    });
  }

  });


   if (performance.navigation.type == 2) {
    console.info( "This page is reloaded" );
    $('#tree-input').prop('checked', false);
  }
  //------- fixed navbar --------//  
/*  $(window).scroll(function(){
    console.log("thinks were scrolling");
    var sticky = $('.header_area'),
    scroll = $(window).scrollTop();

    if (scroll >= 100) sticky.addClass('fixed');
    else sticky.removeClass('fixed');
  });*/


  //------- Price Range slider -------//
  if(document.getElementById("price-range")){
  
    var nonLinearSlider = document.getElementById('price-range');
    
    noUiSlider.create(nonLinearSlider, {
        connect: true,
        behaviour: 'tap',
        start: [ 500, 4000 ],
        range: {
            // Starting at 500, step the value by 500,
            // until 4000 is reached. From there, step by 1000.
            'min': [ 0 ],
            '10%': [ 500, 500 ],
            '50%': [ 4000, 1000 ],
            'max': [ 10000 ]
        }
    });
  
  
    var nodes = [
        document.getElementById('lower-value'), // 0
        document.getElementById('upper-value')  // 1
    ];
  
    // Display the slider value and how far the handle moved
    // from the left edge of the slider.
    nonLinearSlider.noUiSlider.on('update', function ( values, handle, unencoded, isTap, positions ) {
        nodes[handle].innerHTML = values[handle];
    });
  
  }

	    //login and signup success and failure alerts
		if(String(window.location).includes("login-failure")){
			alert("Please enter valid details and try again.");
		}else if(String(window.location).includes("login-success")){
		    alert("Successfully logged in!");
	    }else if(String(window.location).includes("signup-failure")){
			alert("Please enter an email that isn't already in use.");
		}else if(String(window.location).includes("signup-success")){
		    alert("Congrats on your new account!");
		}else if(String(window.location).includes("payment-success")){
		    alert("Thanks for your order!");
		}

		if(String(window.location).includes("myaccount") || String(window.location).includes("login-success") || String(window.location).includes("signup-success")){
			$('#logout-button').on('click', function(){
        		console.log("clicked button");
        		window.location.replace("http://www.klikattatfootwear.com/logout-success");
	    	});
	    	//document.getElementById('account-header').innerHTML = "{{value}}" + "'s Account";
		}

		if(sessionStorage.getItem("Cart") === null){
			console.log("making a shopping cart");
			//two dimensional array to represent product
			var cart = "";
			sessionStorage.setItem("Cart", cart)
		}

		//add to cart button functionality for product summaries like best sellers
		$(".shopping-cart-button").on('click', function(){
			var cartButtonParent = $( this ).parent().parent().parent().parent();
			var cardInfo = cartButtonParent.children()[1];
      		var nameElement = $(cardInfo).children()[1];
      		var name = $(nameElement).text();
      		var urlElement = $(nameElement).children()[0];
      		var url = $(urlElement).attr("href");
      		var priceElement = $(cardInfo).children()[2];
      		var price = $(priceElement).text();
      		var img = $($(this).parent().parent().parent().children()[0]).attr("src");
      		var newProduct = {"ProductName": name, "URL": url, "Price": price, "Quantity": 1, "IMGSRC": img};
      		console.log(newProduct);

      		//need to access cart now that we have product info
      		var cart = sessionStorage.getItem("Cart");
      		if(cart === ""){
				console.log("thinks cart is empty");
				var newCartJson = [newProduct];
				cart = JSON.stringify(newCartJson);
				sessionStorage.setItem("Cart", cart);
			}else{
				console.log("adding to cart");
				var refreshCart = JSON.parse(cart);
				//figure out quantity
				var foundProductInCart = false;
				var j;
				for(j = 0; j < refreshCart.length; j++){
					if(refreshCart[j].ProductName === newProduct.ProductName){
						refreshCart[j].Quantity = parseInt(refreshCart[j].Quantity) + 1;
						foundProductInCart = true;
					}
				}
				if(foundProductInCart == false){
					refreshCart.push(newProduct);
				}
				cart = JSON.stringify(refreshCart);
				sessionStorage.setItem("Cart", cart);
			}

			var newCart = sessionStorage.getItem("Cart");
			console.log(newCart);
			var type = typeof cart;
			console.log("new cart obj type: " + type);
			var currentCartJSON = JSON.parse(newCart);
			console.log(currentCartJSON);
			//want to update website with new cart infomation
			document.getElementById("cart-count").innerHTML = currentCartJSON.length;
		});

		//add sweatshirt to cart
/*		$("#sweatshirt-add-to-cart-button").on('click', function(){
			console.log("called add to cart method");
			console.log(document.getElementById("product-price").innerHTML);
			var quantity = parseInt(document.getElementById("sweatshirt-quantity-count").value)
			var sizeElement = document.getElementById("sweatshirt-size");
			var size = sizeElement.options[sizeElement.selectedIndex].text
			var newProduct = {"ProductName": "Sweatshirt","Size": size,"Price": "$40", "Quantity": parseInt(document.getElementById("sweatshirt-quantity-count").value), "IMGSRC": String(document.getElementById("sweatshirt-product-image").src)};
			var cart = sessionStorage.getItem("Cart");
			console.log(cart);
			//if cart is empty we make it an array of json objects, with just one product

			if(cart === ""){
				console.log("thinks cart is empty");
				var newCartJson = [newProduct];
				cart = JSON.stringify(newCartJson);
				sessionStorage.setItem("Cart", cart);
			}else{
				console.log("adding to cart");
				var refreshCart = JSON.parse(cart);
				//figure out quantity
				var foundProductInCart = false;
				for(i = 0; i < refreshCart.length; i++){
					if(refreshCart[i].ProductName === newProduct.ProductName && refreshCart[i].Size === newProduct.Size){
						refreshCart[i].Quantity = parseInt(refreshCart[i].Quantity) + parseInt(document.getElementById("sweatshirt-quantity-count").value);
						foundProductInCart = true;
					}
				}
				if(foundProductInCart == false){
					refreshCart.push(newProduct);
				}
				cart = JSON.stringify(refreshCart);
				sessionStorage.setItem("Cart", cart);
			}

			var newCart = sessionStorage.getItem("Cart");
			console.log(newCart);
			var type = typeof cart;
			console.log("new cart obj type: " + type);
			var currentCartJSON = JSON.parse(newCart);
			console.log(currentCartJSON);
			//want to update website with new cart infomation
			document.getElementById("cart-count").innerHTML = currentCartJSON.length;
		});*/

		//make sure cart value is set once the page loads
		$('document').ready(function(){
			var cart = sessionStorage.getItem("Cart");
			if(cart !== ""){
				var currentCartJSON = JSON.parse(cart);
				document.getElementById("cart-count").innerHTML = currentCartJSON.length;
			}else{
				document.getElementById("cart-count").innerHTML = 0;
			}
            if(mobileCheck()){
                console.log("javascript thinks we are on mobile");
                //all mobile initializations here
                //change sweatshirt dom order
                //var sweatshirtImage = $("#sweatshirt-images");
                //sweatshirtImage.prev().insertAfter(sweatshirtImage);
                //var logo = $(".navbar-brand");
                //var shoppingCart = $(".nav-shop");
                //shoppingCart.insertAfter(logo);
                //document.getElementById("landing-button-1").innerHTML = "T-Shirts";
                //document.getElementById("landing-button-2").innerHTML = "Sweatshirts";
            }

	        //want to display warning error if user failed to log in correctly
	        console.log($(document.getElementById("cart-login-section")).css("display"));
	        if(String(window.location).includes("cart-login") && $(document.getElementById("cart-login-section")).css("display") === "block"){
	            console.log("displaying!");
	            document.getElementById("cart-login-warning").style.display = "inline";
	        }

	        //reset select fields so that they cooperate in professor section
            var els = document.getElementsByClassName("reset_me");
            for (i = 0; i < els.length; i++) {
                els[i].value = els[i].getAttribute('value');
            }
            //check all checkboxes that need it
            var checkboxes = document.getElementsByClassName("reset_checkbox");
            for (i = 0; i < checkboxes.length; i++) {
                console.log("checkbox value: " + checkboxes[i].getAttribute('value'));
                if(checkboxes[i].getAttribute('value') === '1'){
                    console.log("found a checkbox that needs to be checked");
                    checkboxes[i].checked = true;
                }else{
                    checkboxes[i].checked = false;
                }
            }

            if($("#manage-products-table").length > 0){
                $("#manage-products-table").tableDnD({
                    onDrop: function(table, row) {
                        console.log(table.rows);
                        var arr = [].slice.call(table.rows);
                        var new_order_id_arr = [];
                        //make new order array of the product ids
                        for(i = 1; i < arr.length;i++){
                            new_order_id_arr.push($(arr[i]).find("#product_id").val());
                        }
                        document.getElementById("new_order_array").value = String(new_order_id_arr);
                        document.getElementById("product-reordering-form").submit();
                    }
                });
                //for each design we want to initialize the sizes table
                //var total_design_count =
                //for()
                $(".sizes-table").tableDnD({
                    onDrop: function(table, row) {
                        console.log(table.rows);
                        var arr = [].slice.call(table.rows);
                        var new_size_order_id_arr = [];
                        //make new order array of the product ids
                        for(i = 0; i < arr.length;i++){
                            console.log($(arr[i]).find("#size_id").val());
                            new_size_order_id_arr.push($(arr[i]).find("#size_id").val());
                        }
                        $(table.parentElement).find("#new_size_order_arr").get(0).value = String(new_size_order_id_arr);
                        $(table).parent().find("#size-reordering-form").get(0).submit();
                    }
                });
            }
            console.log('about to init car.');
            //slick carousel initialization
            $(".slick-carousel").slick({
                autoplay: true,
                dots: true,
                pauseOnDotsHover: true,
                arrows: true,
                speed: 800,
                autoplaySpeed: 5000,
                 // the magic
                responsive: [{
                    breakpoint: 1024
                    }, {
                    breakpoint: 600
                    }, {
                    breakpoint: 300
                    }]
            });
            console.log('finished carousel')
            scrollDown();
		});

    //check if this is the cart page
    if(String(window.location).includes("cart")){
        function displaydifshipping() {
            document.getElementById("differentshippingaddress").style.display = "inline";
            document.getElementById("message").style.display = "none";
            document.getElementById("initialshippingdeets").style.display = "none";
        }

        $('#scroll-to-checkout').on('click', function(){
        var checkoutheight = document.getElementById("discount-section").getBoundingClientRect().top;
        console.log(checkoutheight);
        var offset = 130;
        console.log(mobileCheck());
        if (mobileCheck()){
            offset = 80;
        }
        checkoutheight = checkoutheight - offset;
        console.log(checkoutheight);
		$('body,html').animate({
			scrollTop: checkoutheight
		}, 600);
	    });

	    //subtotal calculation:
		//want to change this everytime quantity changes on an item, we remove an item and on page load.
		function updateSubtotal() {
			//using the session storage cart object we are going to add up the total price to everything in the cart
			//first we need the cart object
			console.log("called update subtotal");
			//get all current prices added up
			var totalPrice = 0;
			var cart = sessionStorage.getItem("Cart");
			console.log(cart);
			if(cart !== ''){
				var cartArray = JSON.parse(cart);
				console.log(cartArray);
				console.log(cartArray.length);
				//go through each element in cart array to get subtotal
				for(i = 0; i < cartArray.length; i++){
					var price = Number(cartArray[i].Price.replace(/[^0-9.-]+/g,""));
					var quantity = parseFloat(cartArray[i].Quantity);
					var productTotal = price * quantity;
					console.log(price);
					console.log(quantity);
					console.log(productTotal);
					totalPrice += productTotal;
				}
				console.log(totalPrice);
				totalPrice = totalPrice.toFixed(2);
				totalPrice = "$" + totalPrice;
				$('#subtotal-value').html(totalPrice);
				updateCheckoutTotal();
			}
		}

		//paypal css, css for paypal
	    $('document').ready(function(){
            //footer styling
            //document.getElementById("footer-section").style.position = "relative";
            //document.getElementById("footer-section").style.left = "500px";
            //document.getElementById("footer-section").style.width = "150%";
            updateSubtotal();
        });
		//first we need to clone the default element

		var cart = sessionStorage.getItem("Cart");
		if(cart !== ""){
			var currentCartJSON = JSON.parse(cart);
			var firstElement = $("#cart-product-list").children()[0];
			console.log(currentCartJSON.length);

			//make a clone of a sample product list element so we can copy it and alter the values to our liking
			var cloneOfElement = firstElement.cloneNode(true);
			$(document.getElementById("default-element")).remove();
			console.log(cloneOfElement);
			//goes through all the elements in the cart and creates an element for each
			var i;
			for(i = 0; i < currentCartJSON.length;i++){
				//next we need to alter the new copy of the element with the right info
				$(cloneOfElement).find('#product-name').html(currentCartJSON[i].ProductName);
				$(cloneOfElement).find('#product-id').html(currentCartJSON[i].ProductID);
				$(cloneOfElement).find('#unit-price').html(currentCartJSON[i].Price);
				$(cloneOfElement).find('#quantity').attr("value", currentCartJSON[i].Quantity);
				console.log(currentCartJSON[i].IMGSRC);
				$(cloneOfElement).find("#product-img").attr("src", currentCartJSON[i].IMGSRC)
				$(cloneOfElement).find('#product-link').attr("href", "/");
				$(cloneOfElement).find('#product-design').html(currentCartJSON[i].Design);
				//console.log($(cloneOfElement).find('#product-link').attr("href"));
				$(cloneOfElement).find("#product-size").html(currentCartJSON[i].Size);
				var price = Number(currentCartJSON[i].Price.replace(/[^0-9.-]+/g,""));
				var quantity = Number(currentCartJSON[i].Quantity);
				var totalProductPrice = price * quantity;
				totalProductPrice = "$" + totalProductPrice;
				console.log(totalProductPrice);
				$(cloneOfElement).find('#product-total-price').html(totalProductPrice);
				$(cloneOfElement).attr("id",("Product" + String(i)))
				document.getElementById("cart-product-list").appendChild(cloneOfElement);
				console.log("after appended element");
				cloneOfElement = firstElement.cloneNode(true);
				$(cloneOfElement).attr("style", "");
			}
			console.log("here");
		}else{
			//if there is nothing in the cart we need to clean up the cart page and make everything kosher
			console.log("here!");
			document.getElementById("default-element").style.display = "none";
			var checkoutSampleProduct = $("#checkout-product-list").children()[0];
			console.log(checkoutSampleProduct);
			$(checkoutSampleProduct).hide();
			$("#total").text("$" + 0);
			$('#subtotal-value').text("$" + 0);
		}

        function  quantityUpdate(inputElement) {
  			console.log("called quantity keyup function");
  			var input = parseFloat(inputElement.val());
  			console.log("input: " + input);
  			if(Number.isInteger(input) === true){
  			    //grab the elements associated with our current quantity input
				var parent = inputElement.parent().parent().parent();
				var totalElement = $( parent ).find("#product-total-price");
				var priceElement = $( parent ).find("#unit-price");
				var nameElement = $( parent ).find('#product-name');
				var name = $(nameElement).text();
				var size = String($(parent).find("#product-size").text());
				var design = String($(parent).find("#product-design").text());
				//grab the amount
				var price = parseFloat( $(priceElement).text().replace(/[^0-9.-]+/g,""));
				var totalPrice = price * input;
				//this "totalPrice" refers to this specific products quantity times its specific price
				//it is NOT the totalPrice for the order
				//cant have negative quantity
				if(totalPrice < 0){
					totalPrice = 0;
				}
				//want two decimals
				totalPrice = totalPrice.toFixed(2);
				totalPrice = "$" + totalPrice;
				totalElement.html(totalPrice);
				//need to change the quantity value with the sessionstorage cart object
				var cart = sessionStorage.getItem("Cart");
				var cartArray = JSON.parse(cart);
				for(i = 0; i < cartArray.length; i++){
					if(cartArray[i].ProductName === name && cartArray[i].Size === size && cartArray[i].Design === design){
						cartArray[i].Quantity = input;
					}
				}
				cart = JSON.stringify(cartArray);
		    	sessionStorage.setItem("Cart", cart);
				updateSubtotal();
  			}

  		}

		//change totals in real time if user changes quantity values in cart page
		$( "input[name='qty']" ).on('keyup', function() {quantityUpdate($( this ))});

        $(".quantity-input").on('click', function() {quantityUpdate($( this ))});

		//clear cart function
		$("#clearCart").click(function clearCart(){
			console.log("called clear cart function");
			var cart = sessionStorage.getItem("Cart");
			cart = "";
			sessionStorage.setItem("Cart", cart);
			location.reload();
		});

		$(".close").click(function removeItem(){
			console.log("called remove item method");
			//need this product's name
			var parent = $( this ).parent().parent().parent();
			console.log(parent);
			var nameElement = $( parent ).find('#product-name')
			console.log(nameElement);
			var name = $( nameElement ).text();
			console.log(name);
			var cart = sessionStorage.getItem("Cart");
			var cartArray = JSON.parse(cart);
			console.log(cartArray);
			//we need to find where the element is in our array so we can remove it at the right place
			var elementIndex = "";
			for(i = 0; i < cartArray.length; i++){
				if(cartArray[i].ProductName === name){
					elementIndex = i;
				}
			}
			cartArray.splice(elementIndex, 1);
			cart = JSON.stringify(cartArray);
		    sessionStorage.setItem("Cart", cart);
		    document.getElementById("cart-count").innerHTML = cartArray.length;
			//we need to update subtotal as well
			updateSubtotal();
			//now that we have removed the item from the cart we need to turn off the display for this item in the visual cart
			$(parent).toggle();
		});

        function updateCheckoutTotal() {
            document.getElementById("discount-list-element").style.display = "none";
            document.getElementById("points-list-element").style.display = "none";
			var elementToClone = $("#checkout-product-list").children()[0];
			console.log(elementToClone);
			var listElementClone = elementToClone.cloneNode(true);
			$( elementToClone ).hide();
			var cart = sessionStorage.getItem("Cart");
			var cartArray = JSON.parse(cart);
			console.log(cartArray);
			var total = 0;
			//want to make sure were not appending new elements to old list, clear list if there is more than one element
			var childrenCount = $("#checkout-product-list").children().length;
			if(childrenCount > 1){
				console.log(childrenCount);
				console.log("thinks that there are already elements here");
				for(i = 1; i < childrenCount; i++){
					var currentListItem = $("#checkout-product-list").children()[i];
					console.log(currentListItem);
					$(currentListItem).hide();
				}
			}
			$(listElementClone).show();
			for(i = 0; i < cartArray.length; i++){
				$(listElementClone).find("#checkout-product-name").text(cartArray[i].ProductName);
				$($(listElementClone).find("#checkout-product-name")).attr("name",("Name" + String(i)));
				$(listElementClone).attr("id",("Product" + String(i)))
				$(listElementClone).find('#checkout-product-link').attr("href", cartArray[i].URL);
				//need to set price of this element
				var price = Number(cartArray[i].Price.replace(/[^0-9.-]+/g,""));
				var quantity = Number(cartArray[i].Quantity);
				var totalProductPrice = price * quantity;
				console.log(totalProductPrice);
				total += totalProductPrice;
				$(listElementClone).find("#product-total-price-total").html("$" + totalProductPrice);
				$($(listElementClone).find("#product-total-price-total")).attr("name",("Price" + String(i)));
				console.log(listElementClone);
				document.getElementById("checkout-product-list").appendChild(listElementClone);
				//prep clone for next iteration
				listElementClone = elementToClone.cloneNode(true);
				$(listElementClone).attr("style", "");
			}

			$("#total").text("$" + total);
		}
	}
});

$('body, html').on('scroll', function(){
    if( $('body,html').is(':animated')){
        return;
    }

    var scrollPos = $('body').scrollTop();
    if(document.getElementsByClassName("hero-image").length > 0){
        var hero_image_height = document.getElementsByClassName("hero-image")[0].clientHeight;
        var menu = document.getElementById("nav-list");
        if(scrollPos > hero_image_height){
            var total_height = document.body.scrollHeight - hero_image_height;
            var position_ratio = scrollPos / total_height;
            var link_count = menu.children.length;
            var link_to_highlight = Math.floor(link_count * position_ratio);
            blankNavBar(menu);
            menu.children[link_to_highlight].children[0].style.color = primary_color;
        }else{
            blankNavBar(menu);
        }
    }
});

function blankNavBar(navbar){
    for(i = 0; i < navbar.children.length;i++){
        navbar.children[i].children[0].style.color = "black";
    }
}

function setPoints(element){
	console.log("called set points");
	console.log(element.value);
	document.getElementById("points-to-be-redeemed").innerHTML = "Points to be redeemed: " + element.value;
    //also want to set total preview:
    var newTotal = Number(String(document.getElementById("subtotal-value").innerHTML).slice(1)) - (Number(element.value) * .50);
    document.getElementById("total-after-points").innerHTML = "Your Total After Points: " + "$" + newTotal.toFixed(2);
}

function addToCart(button){
    //do animation on click
    $(button).text("Added to Cart!");
    //
    var thisProductInfo = $(button).closest(".s_product_inner");
    var current_design_index = $(thisProductInfo).find('.slick-carousel').slick('slickCurrentSlide');
    if($(button).closest(".product_image_area").find(".primary-image").length > 0){
        //there is a primary product image
        //first we want to ask if the index is zero
        //0 -> 0
        //1 -> 0
        //2 -> 1

        if(current_design_index !== 0){
            current_design_index--;
        }
    }
    var quantity = parseInt($(thisProductInfo).find('#t-shirt-quantity-count').val());
    console.log("current design index: " + current_design_index);
    var size = $(thisProductInfo).find("#t-shirt-size" + current_design_index + " option:selected").val();
    if(size === undefined){
        size = "N/A";
    }
    var productName = String($(thisProductInfo).find("#product-name").text());
    var productPrice = String($(thisProductInfo).find("#product-price").text());
    var thisProductImage = $(thisProductInfo).find(".primary-image").attr('src');
    var thisProductDesign = $(thisProductInfo).find('.design-name').text();
    var size_index = $(thisProductInfo).find(".active-sizes").children().eq(0).prop('selectedIndex');
    console.log("size index: " + size_index);
    console.log("design id element: ");
    console.log($(thisProductInfo).find('.design_names').children().eq(current_design_index).find(".size-ids"));
    var thisSizeID = $(thisProductInfo).find('.design_names').children().eq(current_design_index).find(".size-ids").children().eq(size_index).text();
    var newProduct = {"ProductName": productName,"Size": size,"Price": productPrice, "Quantity": String(quantity), "IMGSRC": String(thisProductImage), "Design": thisProductDesign, "SizeID": thisSizeID};
    var cart = sessionStorage.getItem("Cart");
    console.log(cart);
    //if cart is empty we make it an array of json objects, with just one product
    button.parentElement.children[1].style.display = "inline";
    if(cart === ""){
        console.log("thinks cart is empty");
        var newCartJson = [newProduct];
        cart = JSON.stringify(newCartJson);
        sessionStorage.setItem("Cart", cart);
    }else{
        var refreshCart = JSON.parse(cart);
        //figure out quantity
        var foundProductInCart = false;
        for(i = 0; i < refreshCart.length; i++){
            if(refreshCart[i].ProductName === newProduct.ProductName && refreshCart[i].Size === newProduct.Size && refreshCart[i].Design === newProduct.Design){
                refreshCart[i].Quantity = parseInt(refreshCart[i].Quantity) + parseInt(document.getElementById("t-shirt-quantity-count").value);
                foundProductInCart = true;
            }
        }
        if(foundProductInCart == false){
            refreshCart.push(newProduct);
        }
        cart = JSON.stringify(refreshCart);
        sessionStorage.setItem("Cart", cart);
    }

    var newCart = sessionStorage.getItem("Cart");
    console.log(newCart);
    var type = typeof cart;
    console.log("new cart obj type: " + type);
    var currentCartJSON = JSON.parse(newCart);
    //want to update website with new cart infomation
    document.getElementById("cart-count").innerHTML = currentCartJSON.length;
    //$(button).text("Add to Cart");
    setTimeout(function(){
        $(button).text("Add to Cart");
    },1500);
}



function applyPoints(){
    document.getElementById("discount-list-element").style.display = "none";
    //updateCheckoutTotal()
    //we want to make sure that we're not going to loose money on this order
    var totalAfterPoints = Number(String(document.getElementById("total-after-points").innerHTML).slice(26));
    var totalAfterPointsCopy = totalAfterPoints;
    var warningElement = document.getElementById("points-error-warning");
    warningElement.display = "none";
    console.log("total after points: " + totalAfterPoints);
    if(totalAfterPoints < 0){
        warningElement.innerHTML = "We're sorry, your order total cannot be less than zero";
        warningElement.style.display = "inline";
        warningElement.style.color = "red";
        console.log("thought total would be negative after points");
    }else{
        //apply points to total since we have a valid amount being spent

        document.getElementById("points-list-element").style.display = "inline";
        var currentTotal = Number(String(document.getElementById("subtotal-value").innerHTML).slice(1));
        document.getElementById("total-points-savings").innerHTML = "$" + (currentTotal - totalAfterPoints).toFixed(2);
        document.getElementById("points-earned").innerHTML = (totalAfterPoints * .1).toFixed(2);
        //make sure to check if we are planting a tree!
        if(document.getElementById("tree-input").checked){
            //they would like to plant a tree
            totalAfterPoints++;
        }
        document.getElementById("total").innerHTML = "$" + totalAfterPoints.toFixed(2);
    }
}

function applyDiscount(discounts){
    //updateCheckoutTotal();
    console.log("called apply discount");
    console.log(discounts);
    var discountCode = String(document.getElementById("discount-code-input").value);
    //check given code against all discount codes in DB
    var valid = false;
    var lastI = ""
    for(i = 0; i < discounts.length;i++){
        console.log(discounts[i]);
        if(discounts[i][1] === discountCode){
            valid = true;
            lastI = i;
            break;
        }
    }
    //if it is a valid one we want to go ahead and subtract that amount from the total
    //we also want to check that we have not already entered a discount code
    //first we have to get how much the discount code actually takes off the order, this can be either a dollar amount or a percentage, based also on the document
    if(valid){
        console.log("thinks this is a valid discount");
        var currentTotal = Number(String(document.getElementById("subtotal-value").innerHTML).slice(1));
        var newTotal = "";
        //could be a percentage discount or a cash amount
        if(discounts[lastI][3] === "cash"){
            newTotal = currentTotal - Number(discounts[lastI][2]);
        }else if(discounts[lastI][3] === "percentage"){
            newTotal = currentTotal * (1 - Number(discounts[lastI][2]));
        }

        if(newTotal >= 0){
            document.getElementById("discount-list-element").style.display = "inline";
            document.getElementById("discount-savings").innerHTML = "$" + String(currentTotal - newTotal);
            document.getElementById("total").innerHTML = "$" + newTotal.toFixed(2);
        } else {
            var warningElement = document.getElementById("discount-warning");
            warningElement.innerHTML = "We're sorry, your order total cannot be less than zero.";
            warningElement.style.display = "block";
        }
    }
}

var locations2D = [];
var orders = [];
function showShippingOrders (arrayOfOrders, arrayOfLocations, arrayOfEvents){
    console.log("array of orders length: " + arrayOfOrders.length);
    var firstElement = $("#shipping-orders-list").children()[0];
    var cloneOfFirstElement = firstElement.cloneNode(true);
    $(firstElement).remove();
    var thisOrderTotal
    console.log(arrayOfEvents);
    for(i = 0;i < arrayOfOrders.length;i++){
        console.log(arrayOfLocations[i].length);
        if(arrayOfOrders[i]["State"] === "Yet to Ship"){
            console.log("thinks it found an order that has yet to ship");
            //orders with no tracking history
            $(cloneOfFirstElement).find("#order-id").html("Order ID: " + arrayOfOrders[i]["OrderID"]);
            $(cloneOfFirstElement).find("#event").html(arrayOfEvents[i]);
            console.log(arrayOfOrders[i]);
            $(cloneOfFirstElement).find("#date").html("Date: " + arrayOfOrders[i]["OrderDate"]);
            thisOrderPrice = 0;
            for(j = 0; j < arrayOfOrders[i]["ProductPrices"].length;j++){
                 thisOrderPrice += Number(String(arrayOfOrders[i]["ProductPrices"][j]).slice(1));
                $(cloneOfFirstElement).find("#product-list").append("<li>" + arrayOfOrders[i]["ProductNames"][j] + "<span style='margin-left: 50px'>" + arrayOfOrders[i]["ProductPrices"][j] + "</span></li>");
            }
            $(cloneOfFirstElement).find("#total-price").html("Total Price: " + "<span style='margin-left: 50px;'>$" + thisOrderPrice + "</span>");
            //document.getElementById("orders-awaiting-shipment").appendChild(cloneOfFirstElement);
            document.getElementById("shipping-orders-list").appendChild(cloneOfFirstElement);
            console.log(arrayOfLocations[i]);
        }else{
            //shipping or shipped orders
            $(cloneOfFirstElement).find("#order-id").html("Order ID: " + arrayOfOrders[i]["OrderID"]);
            $(cloneOfFirstElement).find("#event").html(arrayOfEvents[i]);
            console.log(arrayOfOrders[i]);
            $(cloneOfFirstElement).find("#date").html("Date: " + arrayOfOrders[i]["OrderDate"]);
            var thisOrderPrice = 0;
            for(j = 0; j < arrayOfOrders[i]["ProductNames"].length;j++){
                thisOrderPrice += Number(String(arrayOfOrders[i]["ProductPrices"][j]).slice(1));
                $(cloneOfFirstElement).find("#product-list").append("<li>" + arrayOfOrders[i]["ProductNames"][j] + "<span style='margin-left: 50px'>" + arrayOfOrders[i]["ProductPrices"][j] + "</span></li>");
            }
            $(cloneOfFirstElement).find("#total-price").html("Total Price: " + "<span style='margin-left: 50px;'>$" + thisOrderPrice + "</span>");
            document.getElementById("shipping-orders-list").appendChild(cloneOfFirstElement);
        }
        locations2D[i] = arrayOfLocations[i];
        orders[i] = arrayOfOrders[i];
        cloneOfFirstElement = firstElement.cloneNode(true);
    }
    initMap();
}
var maps = [];
var markers = [];
var shipmentPath = [];
function initMap(){
    console.log("called init map");
    var myLatAndLong = {lat: -40, lng: 50}
        //console.log($(cloneOfFirstElement).children[0]);
    var mapElements = document.getElementsByClassName("map");
    console.log(mapElements);
    for(i = 0; i < locations2D.length;i++){
        for(j = 0; j < locations2D[i].length;j++){
            console.log(locations2D[i].length);
            var newLat = Number(String(locations2D[i][j]).split(",")[0]);
            var newLng = Number(String(locations2D[i][j]).split(",")[1]);
            locations2D[i][j] = {lat: newLat, lng: newLng}
            if(j === 0){
                myLatAndLong = locations2D[i][j];
            }
        }
        //console.log(myLatAndLong);
        if(mapElements[i] == undefined){
            console.log(i);
            console.log(maps[i]);
        }
        maps[i] = new google.maps.Map(mapElements[i], {
            zoom: 4,
            center: myLatAndLong
        });

        markers[i] = new google.maps.Marker({
            position: myLatAndLong,
            map: maps[i],
            title: "Your Package"
        });

        console.log(locations2D[i]);
        shippingLine = new google.maps.Polyline({
          path: locations2D[i],
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });

        shippingLine.setMap(maps[i]);
    }
    var orderElements = $("#shipping-orders-list").children();

    for(k = 0; k < orderElements.length;k++){
        if(orders[k]["State"] === "Shipping"){
            document.getElementById("shipping-orders-list").appendChild(orderElements[k]);
        }else if(orders[k]["State"] === "Yet to ship"){
            //very different conditions for our elements with this case
            document.getElementById("orders-awaiting-shipment").appendChild(orderElements[k]);
        }else if(orders[k]["State"] === "Shipped"){
            document.getElementById("shipped-orders-list").appendChild(orderElements[k]);
        }
    }
    locations2D = []
}

function accountPageLoadingBarActivate (element){
console.log(element.text);
    if(element.text !== "My Account"){
        $("#account-loading-wheel").toggle();
        $("#loading-explanation").toggle();
    }
}

function showSettingsPopUp(){
    document.getElementById("myModal").style.display = "block";
}

function validateForm() {
  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;
  var subject = document.getElementById("subject").value;
  var message = document.getElementById("message").value;
  if (name == "") {
    alert("Name must be filled out");
    return false;
  }else if(subject == ""){
    alert("Subject must be filled out");
    return false;
  }else if(message == ""){
    alert("Message must be filled out");
    return false;
  }
}

function formatForm(){
    console.log("called format form");
    var nameElements = document.getElementsByClassName("checkout-product-name");
    console.log(nameElements);
    var priceElements = document.getElementsByClassName("checkout-product-price");
    console.log(priceElements);
    for(i = 1; i < nameElements.length;i++){
         console.log(nameElements[i].value);
         $('<input />').attr('type', 'hidden')
              .attr('name', "Name" + String(i - 1))
              .attr('value', $(nameElements[i]).html())
              .appendTo('#cart-contents-form');
         $('<input />').attr('type', 'hidden')
              .attr('name', "Price" + String(i - 1))
              .attr('value', $(priceElements[i]).html())
              .appendTo('#cart-contents-form');
    $('<input />').attr('type', 'hidden')
         .attr('name', "Points")
         .attr('value', $(document.getElementById("points-earned")).html())
         .appendTo('#cart-contents-form');
    }
    return true;
}

function clickedTreeBox(element){
    console.log("thinks you clicked the tree checkbox!");
    console.log("Checked? " + element.checked);
    var total = Number(String(document.getElementById("total").innerHTML).substring(1));
    if(element.checked){
        document.getElementById("tree-cost").innerHTML = "$1";
        document.getElementById("total").innerHTML = "$" + String(total + 1);
    }else{
        document.getElementById("tree-cost").innerHTML = "$0";
        document.getElementById("total").innerHTML = "$" + String(total - 1);
    }
}

function browse(){
    var scrollDistance = 710;
    //need to make sure were not on mobile
    if(mobileCheck()){
        scrollDistance = 750;
    }
    $('body,html').animate({
        scrollTop: scrollDistance
    }, 1000, function() {
        // Animation complete.
    });
}

function scrollDown(){
    console.log("in scroll down");
    //we only want to scroll down if they
    //first we want to get all the navbar product links
    $(window).scrollTop(0);
    var product_index = window.location.pathname.replace(/^\/([^\/]*).*$/, '$1');
    if(document.getElementById("product" + String(product_index)) !== null){
        var relevant_product_top_dist = document.getElementById("product" + String(product_index)).getBoundingClientRect().top;
        //relevant_product.scrollIntoView();
        var offset = 130;
        console.log(mobileCheck());
        if (mobileCheck()){
            offset = 80;
        }
        console.log("offset: " + offset);
        relevant_product_top_dist = relevant_product_top_dist - offset;
        console.log("scroll distance: " + relevant_product_top_dist);
        $('body,html').animate({
            scrollTop: relevant_product_top_dist
        }, 1000, function() {
            // Animation complete.
        });
    }
}

function browseSweatshirts(){
    var scrollDistance = 1350;
    if(mobileCheck()){
        console.log("thinks its mobile");
        scrollDistance = 1550;
    }
    console.log("scroll distance: " + scrollDistance);
    $('body,html').animate({
        scrollTop: scrollDistance
    }, 1000, function() {
        // Animation complete.
    });
}

//checks to see if we are on mobile in javascript
function mobileCheck(){
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        return true;
    }
    return false;
}

function showThisOrderItems(button){
    var item_list = $(button).parent().find(".item-list");
    //console.log(item_list);
    $(button).hide();
    item_list.show();
}

function showThisProductDesigns(button){
    var item_list = $(button).parent().parent().find(".design-list");
    //console.log(item_list);
    var closest_table = $(button).closest("table");
    var closest_table_client_width = $(closest_table).width();
    $(button).hide();
    item_list.show();
    closest_table.scrollLeft(closest_table_client_width);
    //we also want to turn off the reordering functionality for
    //for each row in the main table product table we want to add the class
    //$("#manage-products-table tr").addClass("nodrag nodrop");
    //$("#sizes-table tr").removeClass("nodrag nodrop");
}

function closeThisItemSection(button){
    var item_list = $(button).parent().parent().find(".item-list");
    //console.log(item_list);
    $(button).parent().parent().find(".show-items-button").show();
    $(item_list).hide();
}

function closeThisDesignSection(button){
    var item_list = $(button).parent().hide();
    //console.log(item_list);
    $(button).parent().parent().find(".show-items-button").show();
}

function submitOrderNote(button){
    var note = $(button).parent().find(".customer-note-textarea").val();
    $('<input />').attr('type', 'hidden')
    .attr('name', "CustomerNote")
    .attr('value', note)
    .appendTo('#cart-contents-form');
}

$('.slick-carousel').on('beforeChange', function(event, slick, currentSlide, nextSlide){
    //we want to ask if there is a primary image first
    var design_index = nextSlide;   //we want to determine what design we want to show

    //if there is a primary product image
    var product_area = $(event.target).closest(".product_image_area");
    var this_product_design_icons = $(product_area).find("#design-selection");
    if($(product_area).find(".primary-image").length > 0){
        //there is a primary product image
        //first we want to ask if the index is zero
        //0 -> 0
        //1 -> 0
        //2 -> 1

        if(nextSlide !== 0){
            design_index--;
        }
    }


    //else there is no primary product image and we simply do nothing
    //now that we have our design index we want to have the correct design icon highlighted and the correct design name show

    //fist we want to blank the border of all the icons
    $(this_product_design_icons).children().css("border", "unset");
    var current_icon = $(this_product_design_icons).children().eq(design_index);
    $(current_icon).css("border", ("2px solid" + primary_color));

    //now we want to set the name of the design shown
    var design_names = $(product_area).find(".design_names");
    if($(design_names).children().length > 0){
        var current_design_name = $(design_names).children().eq(design_index).children().eq(0).html();
        $(product_area).find(".design-name").html(current_design_name);
    }

    //we want to display the sizes associated with this product
    var current_size_drop_down = $(product_area).find(".active-sizes");
    $(current_size_drop_down).removeClass("active-sizes");
    $(product_area).find(".size-dropdowns").children().eq(design_index).addClass("active-sizes");
    //now that we have chanes the sizes lets ask if the currently shown one is in stock
    var size_index = $(product_area).find(".active-sizes").children().eq(0).prop('selectedIndex');
    if($(design_names).children().eq(design_index).find(".size_inventories").children().eq(size_index).length > 0){
        var this_permutation_inventory_count = Number($(design_names).children().eq(design_index).find(".size_inventories").children().eq(size_index).html());
        //now that we have this index, lets use it to indicate if this permutation is in stock
        if(this_permutation_inventory_count > 0){
            $(product_area).find(".product-in-stock").html("In Stock");
        }else {
            $(product_area).find(".product-in-stock").html("Out of Stock");
        }
    }else{
        $(product_area).find(".product-in-stock").html("");
    }
});

//when the customer changes designs with the icons
function goToSlide(button){
    //first we want the product associated with this button
    var product_area = $(button).closest(".product_image_area");
    var design_index = Number($(button).index());

    //if there is a primary product image we want to add one to the index so that we are actually showing the right slide
    if(doesCurrentProductHaveImage(product_area)){
        design_index++;
    }

    //we want to change the icon border and go to the right carousel slide
    $(button).parent().children().css("border", "unset");
    var current_icon = $(button).parent().children().eq(design_index);
    $(current_icon).css("border", ("2px solid" + primary_color));
    $(product_area).find('.slick-carousel').slick('slickGoTo', design_index);
}

function doesCurrentProductHaveImage(product){
    if($(product).find(".primary-image").length > 0){
        return true;
    }else{
        return false;
    }
}

//when the customer changes sizes with the drop down
//we are basically only doing an inventory check here
$('select').change(function(){
    var product_area = $(this).closest(".product_image_area");
    var size_index = $(this).prop('selectedIndex');
    var design_index = $(product_area).find('.slick-carousel').slick('slickCurrentSlide');
    if(doesCurrentProductHaveImage(product_area)){
        //if so we want to subtract from the design index
        if(design_index !== 0){
            design_index--;
        }
    }
    var design_names = $(product_area).find(".design_names");
    var this_permutation_inventory_count = Number($(design_names).children().eq(design_index).find(".size_inventories").children().eq(size_index).html());
    //now that we have this index, lets use it to indicate if this permutation is in stock
    if(this_permutation_inventory_count > 0){
        $(product_area).find(".product-in-stock").html("In Stock");
    }else {
        $(product_area).find(".product-in-stock").html("Out of Stock");
    }
});