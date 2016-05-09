def default_message_generator(message='default text', **kwargs):
    
    item = {'fallback': message, 'pretext': message}
    
    slack = kwargs.get('slack')
    
    if slack and isinstance(slack, dict):
        if 'color' in slack:
            item['color'] = slack.get('color')
            
        if 'title' in slack:
            item['title'] = slack.get('title')
            
        if 'pretext' in slack:
            item['pretext'] = slack.get('pretext')
            
        if 'text' in slack:
            item['text'] = slack.get('text')
             
        if 'fields' in slack and isinstance(slack.get('fields'), dict):
            item['fields'] = []
            for key, value in slack.get('fields').items():
                item['fields'].append({
                    'title': key,
                    'value': value,
                    'short': False,
                })
        
    slack_attachments = [item]

    return slack_attachments
