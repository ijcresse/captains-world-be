class SearchQuery:
    
    #find intersection set of reviews from given tag list
    #tag ids must be a string formatted as such:
    #"'tag1', 'tag2', 'tag3', 'tag4'"
    @staticmethod
    def get_reviews_from_tags_query(tag_ids):
        num_tags = len(tag_ids)
        
        ids = []
        for id in tag_ids:
            ids.append(str(id['c_id']))

        tag_param = "', '".join(ids)
        tag_param = "'{}'".format(tag_param)

        return f"""
            SELECT d.c_id, d.c_name, d.c_sake_type, d.c_date_enjoyed, d.c_image_url 
            FROM t_drink d, t_drink_tag dt, t_tag t 
            WHERE (t.c_id IN ({tag_param})) 
            AND t.c_id = dt.fk_tag_id 
            AND d.c_id = dt.fk_drink_id
            GROUP BY d.c_id
            HAVING COUNT( d.c_id )={num_tags}
            """

    @staticmethod
    def get_reviews_from_params_query(name, type):
        if name is None:
            return f"""
                SELECT c_name, c_sake_type, c_date_enjoyed, c_description, c_image_url 
                FROM t_drink  
                WHERE c_sake_type = '{type}'
                """
        elif type is None:
            return f"""
                SELECT c_name, c_sake_type, c_date_enjoyed, c_description, c_image_url 
                FROM t_drink 
                WHERE c_name LIKE '%{name}%'
                """
        else:
            return f"""
                SELECT c_name, c_sake_type, c_date_enjoyed, c_description, c_image_url 
                FROM t_drink 
                WHERE c_name LIKE '%{name}%' 
                AND c_sake_type = '{type}'
                """