# 检查电脑ip变化

设置开机启动后，自动检查电脑ip是否变化，如果变化则发送邮件提醒

### windows

在bat文件中写入运行脚本的python命令，将bat文件放到`启动`文件夹下

### linux

1. 编写脚本形如下

```bash
#!/bin/sh 

cd <脚本所在路径>
python3 get_host_ip.py  >> ./log.txt
echo ' '>> ./log.txt
```

2. 修改`\etc\rc.local`文件

```bash
sleep 40s  # 适当延时，使得依赖完全启动，否则python脚本不运行
bash <上面脚本路径>

exit 0
```

3. `sudo chmod +x \etc\rc.local`