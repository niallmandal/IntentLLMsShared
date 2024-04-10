import json
import os
import httpx
from openai import OpenAI
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from cowswap.order import Order
load_dotenv()

# Function to convert transaction text to JSON using appropriate schema
def convert_transaction(transaction_text, swap_schema, limit_order_schema):
    api_key = os.getenv("OPENAI_CIRCLE_API_KEY")
    if api_key is None: 
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI(
            api_key=api_key,
            base_url="https://chatai.circle.com/api/proxy/open_ai/v1",
            http_client=httpx.Client(
                follow_redirects=True,
                verify=False,
            ),
        )

    # System message explaining the task and giving hints for each schema
    system_message = {
        "role": "system",
        "content": "Determine if the following transaction text is for a token swap or a limit order. Then fill out the appropriate JSON schema based on the transaction details. Use the token swap schema for swaps and the limit order schema for limit orders. All prices are assumed to be in USD."
    }

    # Messages to set up Schema
    swap_schema_message = {
        "role": "system",
        "content": "Token Swap Schema:\n" + json.dumps(swap_schema, indent=2)
    }
    limit_order_schema_message = {
        "role": "system",
        "content": "Limit Order Schema (the limit price is set based on the price the user specifies for the desired asset. If no expiry is indicated for the order, leave it blank):\n" + json.dumps(limit_order_schema, indent=2)
    }

    date_message = {
        "role": "system",
        "content": "The current datetime is: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ". Incorporate this value if the user specifies a limit order for a relative date (i.e. 7 days from now)"
    }

    intructions_schema_message = {
        "role": "system",
        "content": "The outputted JSON should be an instance of the schema. It is not necessary to include the parameters/contraints that are not directly related to the data provided."
    }

    # User message with the transaction text
    user_message = {
        "role": "user",
        "content": transaction_text
    }

    # Sending the prompt to ChatGPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={ "type": "json_object" },
        messages=[system_message, swap_schema_message, limit_order_schema_message, date_message, intructions_schema_message, user_message]
    )

    # Extracting the last message from the completion
    filled_schema_text = completion.choices[0].message.content.strip()
    try:
        filled_schema = json.loads(filled_schema_text)
    except json.JSONDecodeError:
        print("Error in decoding JSON. Response may not be in correct format.")
        filled_schema = {}

    filled_schema["recipientAddress"] = "0xd90830099281B7F58eA54f6aD27665e35653CB65"

    sellToken = tokens[filled_schema["fromAsset"]]
    buyToken = tokens[filled_schema["toAsset"]]
    amount = filled_schema["amount"]
    address = filled_schema["recipientAddress"]
    limitOrder = filled_schema.get("limitOrder", None)
    validTo = limitOrder.get("validTo", int((datetime.now() + relativedelta(months=+6)).timestamp()))
    
    # print(f"Transaction Details:\nAmount: {amount} \nSell:{sellToken}\nBuy: {buyToken}\nRecipient Address: {address} \n Limit Order: {limitOrder}")
    if limitOrder:
        order = Order()\
            .withSellToken(sellToken)\
            .withBuyToken(buyToken)\
            .withReceiver(address)\
            .withSellAmount(amount)\
            .withBuyAmount(0)\
            .withValidTo(validTo)\
            .withFeeAmount(0)\
            .withKind("buy")\
            .withPartiallyFillable(False)\
            .swithSellTokenBalance("0")\
            .withBuyTokenBalance("0")\
            # .post()
        # print(Order.json(order))
    else: #swap order
        order = Order()\
            .withSellToken(sellToken)\
            .withBuyToken(buyToken)\
            .withReceiver(address)\
            .withSellAmount(amount)\
            .withBuyAmount(0)\
            .withValidTo(0)\
            .withFeeAmount(0)\
            .withKind("sell")\
            .withPartiallyFillable(False)\
            .swithSellTokenBalance("0")\
            .withBuyTokenBalance("0")\
            # .post()
        # print(Order.json(order))

    return Order.json(order)

# Example usage
# transaction_text = "I want to swap my 10 SOL for SOL if it hits $25.00 or above"
swap_schema_path = 'swap.json'
limit_order_schema_path = 'limit_swap.json'

# Load the JSON schemas
with open(swap_schema_path, 'r') as file:
    swap_schema = json.load(file)
with open(limit_order_schema_path, 'r') as file:
    limit_order_schema = json.load(file)

tokens = {
    "$ETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "$DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "$USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
} #fill




# filled_schema = convert_transaction(transaction_text, swap_schema, limit_order_schema)
# sellToken = filled_schema["fromAsset"]
# buyToken = filled_schema["toAsset"]
# amount = filled_schema["amount"]
# address = filled_schema["recipientAddress"]
# print(json.dumps(filled_schema, indent=4))
# print(f"Transaction Details:\nSell: {amount} {sellToken}\nBuy: {buyToken}\nRecipient Address: {address}")