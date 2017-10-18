# ec2-metadata
Pulls AWS metadata to a file on disk

Example systemd configuration:

```
[Unit]
Description=EC2 metdata agent
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
ExecStartPre=-/usr/bin/docker stop ec2-metdata
ExecStartPre=-/usr/bin/docker rm -f ec2-metadata
ExecStartPre=/usr/bin/docker pull discobean/ec2-metadata
ExecStart=/usr/bin/docker run --name=ec2-metadata --net=host -v /run/metadata:/run/metadata discobean/ec2-metadata:latest

[Install]
WantedBy=multi-user.target
```
