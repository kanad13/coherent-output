# Orders Platform Brief

The orders platform takes orders from a web storefront and a mobile app. Both call the Orders API.

## Services

The Orders API validates each order and writes it to the Orders database. It then publishes an OrderPlaced event to the event bus. The Payments service reads the event and charges the customer through an external card processor. The Fulfilment service reads the same event, reserves stock in the Inventory database, and asks an external carrier to collect the parcel.

## Notifications

The Notification service reads events from the event bus and sends email through an external email provider. It keeps a template store of message documents.
