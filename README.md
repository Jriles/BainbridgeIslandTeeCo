# Customizable E-commerce Website

This is a lightweight customizable e-commerce Flask, SQL, HTML, Javascript, JQuery, CSS and PayPal built ecommerce app.
One version of this app:
https://www.bainbridgeislandteeco.com/

## Table of Contents
1. [Requirements](#requirements)
2. [Design Notes](#design-notes)
3. [Dev Notes](#dev-notes)
4. [Credits](#credits)

### Requirements <a name="requirements"></a>

Make sure to make a business PayPal account to connect to the website, you have to swap out the cdn in base.html. You can easily test the website with a PayPal sandbox account. 

There shouldn't be anything like a CMS, plugins or other things like that as long as you install all the packages you need with:

     pip install your_package_name
### Design Notes <a name="design-notes"></a>

One cool thing about this project is the admin's ability to make a variety of changes to the website like changing the logo, the primary brand color, the main landing image, the products, the designs associated with each product. Admins can also set maintenance mode and keep track of orders, make staff notes on orders and view customer information/notes. The website is also intentionally short in nature, with the idea that with fewer places to get sidetracked users will be driven to the cart/checkout page with less of a loss in conversions. Which reminds me of another design decision with the same goal in mind: the unified cart/checkout page. Customers can write notes about their order, apply for discounts, review their order and checkout all from the cart page. This way more customers aren't lost at another unnecessary bottleneck in the conversion flow. The app was designed to increase user intuitiveness and conversions. There is extensive customizability here thanks to flask's unique power to get applications going quickly. Thins like the shipping policy, company email, products, designs and sizes are all manipulable in the admin page.
### Dev Notes <a name="dev-notes"></a>

     .gitignore
     your_project.ini
     
### Credits <a name="credits"></a>
Built by owner.
