# The Beehyve

Together with the PLCnext Community, we want to create a smart version of a beehive that will improve the lives of bees through intelligent automation and thus make a sustainable contribution to our environment. Bees are indispensable for our ecosystem: they pollinate around 80% of all wild and cultivated plants and thus ensure high-yield harvests as well as an immense variety of food. These are very good and weighty reasons to do something for these industrious insects.

Further information about the project can be found in the [PLCnext Community](https://www.plcnext-community.net/beehyve/).

## Proficloud Data

Measurement data of the Beehyve is sent to the Proficloud. An interactive dashboard of the data can be found [here](https://tsd.proficloud.io/d/2mp1VEy4z/beehyve?orgId=2507&refresh=5s). A login is required to access the dashboard. Therefore, we created a default beehyve user: beehyve@phoenixcontact.com / PW: Beehyve:2023!

The same credentials can be used to interact with the Proficloud's REST interface. You can find an example in python how to fetch data from the Proficloud and store them as a csv file. The script is located in `proficloud_data/fetch_pc_data.py`. Before running it, you should adapt the storage paths.

If you want to create your own solution, you can start with the API description of the REST interface in the
[Proficloud documentation](https://proficloud.io/technical-documentation/#apis-services). Required parameters can be found in the python script.
