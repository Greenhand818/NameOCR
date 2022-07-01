# businesscard

## 功能

- 选择名片允许产生文字的位置区域。
- 根据名片背景和划定的若干区域，在名片上的这些区域内的随机位置产生相应内容的不同大小和不同字体的文字。
- 文字内容的生成，目前只有人名(中英文)和邮箱地址。
- 在图片上产生的文字目前只有单行的人名。

## 运行

- 选择名片允许产生文字的位置区域：

~~~shell
python3 GetBgROI.py --bg_path path/to/your_background
~~~

- 运行生成器：

~~~shell
python3 generator.py --target_path path/to/result_image
					 --ttf_path path/to/your_ttf
					 --email_suffix path/to/your_email_suffix
					 --domain_path path/to/your_net_domain
					 --ch_last_name_path path/to/chinese_last_name
					 --ch_first_name_path path/to/chinese_first_name
					 --en_last_name_path path/to/english_last_name
					 --en_first_name_path path/to/english_first_name
					 -amount 1000
					 --database True if store in mysql
~~~

## 项目文件介绍

​	本项目只实现了中英文人名的生成，并将其生成在指定区域中；实现了邮箱地址的生成。其它，如网址的生成、邮编、电话、公司名称、公司地址等的生成都没有实现。

​	如果想要添加这些功能，可以在generate_word文件夹下的 GenerateNet.py、GeneratePost.py等脚本中进行添加，并在初始化脚本中，根据自己定义的类名进行修改。