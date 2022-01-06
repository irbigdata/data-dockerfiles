db.auth('root', '1234')

db = db.getSiblingDB('logs')

db.createUser(
    {
        user: "lifeweb",
        pwd: "lifeweb123",
        roles: [
            {
                role: "readWrite",
                db: "logs"
            }
        ]
    }
);

db.createCollection('events'); 
db.events.insert( { 
    
        "_id" : ObjectId("5ff43be5b3bcab95ae000001"),
        "all_rating" : 84812,
        "app_name" : "Fast VPN – Free VPN Proxy & Secure Wi-Fi",
        "country" : "iran",
        "app_category" : "Tools",
        "free_rank_change" : 0,
        "star_rating" : 4.2,
        "lf_wrapper" : 1,
        "app_id" : "vpn.fastvpn.freevpn",
        "date" : "2020-10-09",
        "@version" : "1",
        "free_rank" : 1,
        "market" : "google_play",
        "category" : "Overall",
        "company_name" : "FAST VPN",
        "pk" : "4fb54d9296a529a963961a85ae6c0f8e"
    
} )


// db.createUser(
//     {
//         user: "root",
//         pwd: "1234",
//         roles: [
//             {
//                 role: "readWrite",
//                 db: "logs"
//             }
//         ]
//     }
// );