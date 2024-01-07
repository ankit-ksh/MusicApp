from sangeet.extensions import db
from sangeet.models import Track

def content_overview(categories):   # function for showing any content overview and redirecting to a page with all entries by just taking a categories dictionary
    content = {}
    for item in categories:
        table = item['table']
        filter_by = item.get('filter_by', None)
        value = item.get('value', None)
        cat_link = item['cat_link']
        content[cat_link] = {}
        content[cat_link]['title'] = item['title']
        content[cat_link]['cat_link'] = item['cat_link']
        if (filter_by is None):                 # If its the case of returning all items from a table
            query_result = db.session.execute(db.select(table).limit(5)).scalars()
            if (content[cat_link].get('order_by')):
                order_by = content[cat_link].get('order_by')
                query_result = db.session.execute(db.select(table).order_by(getattr(table, order_by)).desc()).limit(5).scalars()
        elif item.get('table_2'):                # if condition will evaluate to true if table_2 attribute exists
            table_2 = item['table_2']
            query_result = db.session.execute(db.select(table).where(getattr(table_2, filter_by).ilike(f"{value}")).limit(5).join_from(table, table_2)).scalars()
        else:   # both of the above and below queries are achiveing case insensitive matching, but in a different way
            query_result = db.session.execute(db.select(Track).where(db.func.lower(getattr(table, filter_by)).ilike(f"{value.lower()}")).limit(5)).scalars()
        query_result = [result for result in query_result]
        content[cat_link]['items'] = query_result
    return content
