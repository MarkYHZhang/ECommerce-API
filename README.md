# Shopify Developer Challenge

Hey there, first of all thank you for reviewing my application. I hope you are having a great day so far :D
This README will be divided into the following two main sections with its subsections:

 - [Design](#design)
	 - [Process Flow](#process-flow)
	 - [Security measures](#security-measures)
	 - [Unit testing](#unit-testing)
 - [Endpoints](#endpoints)
	 - [`/retrieveProducts`](#retrieve-products)
	 - [`/createCart`](#create-cart)
	 - [`/modifyCart`](#modify-cart)
	 - [`/checkoutCart`](#checkout-cart)
	 - [`/discardCart`](#discard-cart)
	 - [`/accessToken`](#access-token)

## Design
### Process Flow
![Design flow](https://raw.githubusercontent.com/MarkYHZhang/markyhzhang.github.io/master/static/img/ShopifyDevChallengeFlow.png)

### Security Measures
External Protection (Cloudflare):
As shown in the diagram above, there are three main protections that Cloudflare offers:

 1. SSL Certification: this ensures a secure HTTPS connection which aims to prevent attackers from intercepting packets that contains access tokens or the content of the API calls.
 2. DDOS Protection: Thank to Cloudflare's DDOS mitigation service, this API service will be prone to these types of attacks that overloads the server with requests.
 3. Origin IP Hiding: The origin server's public IP will be hidden behind Cloudflare's firewall that acts as a "middle man" which takes requests from user and pass them onto the origin server. The benefit of this is that it does not expose origin server's IP which prevents many sorts of attacks. 

Internal Protection (Origin Server):

 1. Cross-Origin Resource Sharing (CORS) headers that specifically allows only GET and POST requests to filter out invalid requests.
 2. Rate Limiter: rate limiting interval is based on each requests (for more detail check the [endpoints](#endpoints) section).
 3. API Token authentication: If this API were to be integrated to a complete online eCommerce, unique temporary tokens will be issued to user browser upon login. (Tokens will expire after every session)

### Unit Testing

 - Database model tests
	 - Product model
	 - Cart model
	 - Token model
 - RESTful endpoint tests
	 - [`/retrieveProducts`](#retrieve-products)
	 - [`/createCart`](#create-cart)
	 - [`/modifyCart`](#modify-cart)
	 - [`/checkoutCart`](#checkout-cart)
	 - [`/discardCart`](#discard-cart)
	 - [`/accessToken`](#access-token)
 
## Endpoints
### Retrieve Products
Access Endpoint: **POST** `/retrieveProducts` 

| Argument | Type | Example | Explanation |
| --- | --- | --- | --- |
| availableInventoryOnly | boolean  | `"availableInventoryOnly": "true"`  | Only return products that have inventory count > 0 |
| all | boolean | `"all": "true"` | This will return all products |
| products | array | `"products":["blue_shirt", "red_shirt"]` | Returns a list of product information based on the input (which is a list of product ids) |

Sample Request:

	{
	  "availableInventoryOnly": "false",
	  "products":[
	    "blue_shirt",
	    "red_shirt"
	  ]
	}

Corresponding Sample Response:

	[
	  {
	    "title": "Blue Shirt",
	    "price": "1000.00",
	    "inventory_count": 10,
	    "product_id": "blue_shirt"
	  },
	  {
	    "title": "Red Shirt",
	    "price": "100.00",
	    "inventory_count": 35,
	    "product_id": "red_shirt"
	  }
	]

### Create Cart
Access Endpoint: **GET** `/createCart`
Sample Request:
Simply visit /createCart endpoint

Corresponding Sample Response:

	{
	  "response": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"
	}

### Modify Cart 
Access Endpoint: **POST** `/modifyCart` 

|Argument|Type |Example | Explanation
|--|--|--|--|
| cart_id|string  |`"cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"`  | This is a mandatory field that identifies which cart is being modified
|items| array | `"items":[{"action": "add", "product_id": "red_shirt", "quantity": 10}]`|This array contains a list of actions for each specified items

Table for item action

|Argument|Type |Example | Explanation
|--|--|--|--|
| action|string|`"action": "add"` or `"action": "remove"`  | This mandatory field specify the action to be performed
|product_id| string| `"product_id": "red_shirt"`|Specifies  the product id of the target product
||||

Sample Request:

	{
	  "cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e",
	  "items": [
	    {
	      "action": "add",
	      "product_id": "red_shirt",
	      "quantity": 10
	    },
	    {
	      "action": "remove",
	      "product_id": "blue_shirt",
	      "quantity": 1
	    }
	  ]
	}

Corresponding Sample Response:

	[
	  {
	    "items": [
	      "red_shirt",
	      "blue_shirt"
	    ],
	    "item_quantities": [
	      "13",
	      "1"
	    ],
	    "cost": "2300.00",
	    "cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"
	  }
	]

### Checkout Cart
Access Endpoint: **POST** `/checkoutCart`
Sample Request:

	{
	  "cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"
	}

Corresponding Sample Response:

	[
	  {
	    "items": [
	      "red_shirt",
	      "blue_shirt"
	    ],
	    "item_quantities": [
	      "13",
	      "1"
	    ],
	    "cost": "2300.00",
	    "cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"
	  }
	]

### Discard Cart
Access Endpoint: **POST** `/discardCart`
Sample Request:

	{
	  "cart_id": "7cc41f04-df61-4a85-8e0d-4decdd2c1a2e"
	}

Corresponding Sample Response:

	{
		"response":  "REMOVED"
	}
