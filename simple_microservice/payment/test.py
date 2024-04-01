import stripe
#Joshua API key 
stripe.api_key = "sk_test_51OyrMORsQ5WaThPekIN8poryHhxBLzXKQ9EhYDvc58oNPSRTKrgpZy3haLx99TBdFw4ktMD27A7MClQI0SfSeZlz00L4z8Mwqf" 
 
#make 2 products one for each event - create separate script
# stripe.Price.create( 
#   currency="sgd", 
#   unit_amount=1000, 
#   lookup_key="event_1", 
#   product_data={"name" : "event_1"} 
# ) 
 
#i give u event id (lookup key) then u create session for me

list_price_result = stripe.Price.list(lookup_keys=["marco"]) 
# print(list_price_result) 
 
the_price_i_need = list_price_result["data"][0] 
the_id_i_need = the_price_i_need["id"] 
 
session = stripe.checkout.Session.create( 
    success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}", 
    line_items=[{"price": the_id_i_need, "quantity": 1}], 
    mode="payment", 
) 

print(session)
session_id= session.id

# print(session_id) 

#session_1 =
#ur1_1 =  
#session_2 =

#create an endpoint that accept a checkout ID and tell me whether its done (paid in payment status)
# print(stripe.checkout.Session.retrieve( 
#         session_id, 
# ))

# print(session["payment_status"])
