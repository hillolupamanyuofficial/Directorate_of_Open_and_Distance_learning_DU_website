class Formatter():

    def NotificationFormatter(datas):
        output = []
        for data in datas:
            notification_data = {
                "title" : data["title"],
                "doc_link" : data["doc_link"]
            }
            output.append(notification_data)
        return output