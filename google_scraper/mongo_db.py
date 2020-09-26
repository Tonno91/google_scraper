from pymongo import MongoClient


def load_dict_to_db(address, port, array):
    """Function to load a dictionary on a specific database on address and port"""
    # Establish connection with the server
    vbv_coll_id = None
    db = conn_to_db(address, port)

    if score_results(db, array):
        print('******************** UPLOADING START ********************')
    else:
        print('The position results are all the same. DB not loaded\n')
        return False

    vbv_coll_id = db.insert_many(array)
    print(vbv_coll_id)
    print('******************** UPLOADING COMPLETED ********************\n')

    return True


def conn_to_db(address, port):
    """Function to connect to the database"""
    try:
        connection_string = "mongodb://" + str(address) + ":" + str(port) + "/"
        connection_string.replace("\n", "")
        client = MongoClient(connection_string)
        return client.local.scrape
    except:
        return False


def score_results(db, array):
    save_to_DB = False
    for current_data in array:
        try:
            prev_result = db.find({"$and": [{"website": current_data["website"]},
                                   {"keyword": current_data["keyword"]},
                                   {"title": current_data["title"]},
                                   {"full_link": current_data["full_link"]}
                                   ]}).sort([('_id', -1)])
            debug = prev_result.count()
            if prev_result.count() == 0:
                print("NEW! Website: {}\tKeyword: {}\tLink: {}\t Not present in DB".format(
                    current_data["website"], current_data["keyword"], current_data["full_link"]))
                save_to_DB = True
            else:
                prev_result = prev_result[0]
                current_data["weight"] = prev_result["weight"] + 1

                if prev_result["position"] != current_data["position"]:
                    current_data["actual_score"] = prev_result["position"] - current_data["position"]

                    print("NEW SCORE:\t{}\nScore: {}\tPosition: {}\t---> {}".format(
                        current_data["base_link"], current_data["actual_score"], prev_result["position"],
                        current_data["position"]))
                    save_to_DB = True
                current_data["total_score"] = prev_result["total_score"] + current_data["actual_score"]
        except Exception as e:
            raise Exception('Exception inside mongoDB:\n' + str(e))
    return save_to_DB


# # WARNING - THIS COMMAND DELETE THE ENTIRE DATABASE - WARNING
# if __name__ == "__main__":
#     address = "localhost"
#     port = "27017"
#     db = conn_to_db(address, port)
#     result = db.delete_many({})
#     print(result.deleted_count)