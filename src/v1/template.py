import settings

from includes.common import Common

class Template:

    def EmailHeader():

        return """
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <meta name=Generator content="Microsoft Word 15 (filtered medium)">
            </head>
            <body style="font-family: sans-serif; background-color: #e1e1e1; margin: 0; padding: 0;">
                <div style="max-width: 525.0pt; margin: 20px auto; background-color: #ffffff; overflow: hidden;">
        """

    def EmailFooter():

        return """
                <div style="text-align: center; padding: 10px; font-size: 12px; color: #666666; background-color: #f9f9f9;">
                    <p style="margin: 5px 0;">Please do not reply to this message. Replies are routed to an unmonitored mailbox.</p>
                    <p style="margin: 5px 0; font-size: 8px; color: #dddddd; text-align: center;">Built by Jawwad Abbasi</p>
                </div>
            </body>
            </html>
        """

    def EmailBatsignal(meta):

        return f"""
            {Template.EmailHeader()}

            <!-- Preview message -->
            <p style="display:none;">{meta.get('Content', 'Please visit our website to get the latest update.')}</p>

            <div style="background-color: #333333; color: #ffffff; text-align: center; padding: 15px;">
                <h1 style="font-size: 20px; margin: 0;">Batsignal</h1>
            </div>

            <div style="padding: 20px; color: #333333; font-size: 14px; line-height: 1.5;">

                <p style="color: #333333; font-weight: bold; font-size: 16px;">{Common.MonthDatetime()}</p>

                <p>Dear members,</p>

                <p class="content">{Common.FormatEmailMessage(meta.get('Content','Please visit our website to get the latest update.'))}</p>

                <p>We thank you for your patience and understanding.</p>
                <p>Best regards,<br>The Bat Family</p>
            </div>

            {Template.EmailFooter()}
        """
    
    def TeamsBatmanIncident(meta):

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "EB2005",
            "summary": "ITSM Incident Reported",
            "sections": [{
                "activityTitle": "ITSM Incident Reported",
                "activitySubtitle": "",
                "activityImage": "https://q5n8c8q9.rocketcdn.me/wp-content/uploads/2019/09/0711_notification_bell_dribble.gif",
                "facts": [
                    {
                        "name": "Incident:",
                        "value": f"[{meta.get('IncidentNumber')}]({settings.BATMAN_URL}/incident?inc={meta.get('IncidentNumber')})"
                    },
                    {
                        "name": "Request ID:",
                        "value": f"[{meta.get('RequestId')}]({settings.BATMAN_URL}/requests?rid={meta.get('RequestId')})"
                    },
                    {
                        "name": "Task ID:",
                        "value": meta.get('TaskId','N/A')
                    },
                    {
                        "name": "Request:",
                        "value": meta.get('RequestAction','N/A')
                    },
                    {
                        "name": "Action:",
                        "value": meta.get('TaskAction','N/A')
                    },
                    {
                        "name": "Microservice:",
                        "value": meta.get('Microservice','N/A')
                    },
                    {
                        "name": "Endpoint:",
                        "value": meta.get('Endpoint','N/A')
                    }
                ],
                "markdown": True
                },

                Template.TeamsFooter(),
            ],
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "View Incident in Batportal",
                    "targets": [{
                        "os": "default",
                        "uri": f"{settings.BATMAN_URL}/incident?inc={meta.get('IncidentNumber')}"
                    }]
                },
                {
                    "@type": "OpenUri",
                    "name": "View Request in Batportal",
                    "targets": [{
                        "os": "default",
                        "uri": f"{settings.BATMAN_URL}/requests?rid={meta.get('RequestId')}"
                    }]
                },
            ]
        }
    
    def TeamsBatmanNotification(meta):

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "EB2005",
            "summary": "TEST",
            "sections": [{
                "activityTitle": "TEST",
                "activitySubtitle": "",
                "activityImage": "https://q5n8c8q9.rocketcdn.me/wp-content/uploads/2019/09/0711_notification_bell_dribble.gif",
                "facts": [
                    {
                        "name": "Date:",
                        "value": Common.Datetime()
                    },
                ],
                "markdown": True
            },

            Template.TeamsFooter(),
            ],
        }
    
    def TeamsBatmanMessage(meta):

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "EB2005",
            "summary": "TEST",
            "sections": [{
                "activityTitle": "TEST",
                "activitySubtitle": "",
                "activityImage": "https://q5n8c8q9.rocketcdn.me/wp-content/uploads/2019/09/0711_notification_bell_dribble.gif",
                "facts": [
                    {
                        "name": "Date:",
                        "value": Common.Datetime()
                    },
                ],
                "markdown": True
            },
            
            Template.TeamsFooter(),
            ],
        }
    
    def TeamsFooter():
        
        return {
            "activityTitle": "**Automation Information**",
            "activitySubtitle": "",
            "facts": [
                {
                    "name": "Developed by:",
                    "value": "Jawwad Abbasi"
                },
                {
                    "name": "Powered by:",
                    "value": "Kodelle Inc."
                }
            ],
            "markdown": True,
        }