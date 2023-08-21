client = Client(TWILIO_SID, TWILIO_AUTH_KEY)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            to="+918800758061",
            from_="+18155679217"
        )