# wakapi-offline-importer

我打算从 Wakapi.dev 转为 self-hosted 的，但是数据自动化导入了一整个下午都没有完成，所以写这个程序，用于从 wakatime 下载的 heartbeats json 文件中直接导入数据到 自部署到wakapi 的 MySQL 数据库里。

I just want to migrate from Wakapi.dev to self-hosted one, but the data automation import took a whole afternoon and still not finished, so I write this program to import data directly from the heartbeats json file downloaded from wakatime to the MySQL database deployed on wakapi.

## Usage

### Setup Your Own Wakapi

See [muety/wakapi](https://github.com/muety/wakapi).  
Use `MySQL` as the database.  
After setup, sign up your account in your own site.

### Download Files From Wakatime

Assume you were using wakapi with wakatime connected, so your heartbeats data is stored duplicated in both wakatime and wakapi. 

#### heartbeat.json

Access [wakatime.com](https://wakatime.com/settings/account), click on the `Download` link of the `Export` panel.

#### user_agent.json

As the `os` and `editor` was saved in separate table with foreign key in heartbeats table, you need to download the `user_agent.json` file from wakatime.

Just access the [API docs site of wakatime](https://wakatime.com/developers#user_agents), click on the `Tri it out` link, copy the JSON you got and save it to a file named `user_agent.json`.

#### machine_name.json

Similar to `user_agent.json`, get it from [here](https://wakatime.com/developers#machine_names).

### Import Data

```bash
pip install -r requirements.txt
```

```bash
python main.py <heartbeat file> <user name> <mysql db host> <mysql db user> <mysql db password> <mysql db name> <start date, such as 2021-03-01> <user_agent file> <machine_name file>
```

That's all you need to do.

### Note

#### Can not see my data in dashboard after import?

Set up you client configuration as the wakapi docs said, and send some new heartbeats to wakapi, then you can see your data in dashboard.
