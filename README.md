# forrabbitmq

installation steps for RHEL 7-8 with python publisher and consumer example.

	1- Login as root.
	2- check repo accesses and python3 installation.
	$ python3 --version
	Python 3.6.8
	İf python3 is not installed on server, install it with code below.
	$ yum install python3
	
	Check repo accesses:
	$ telnet  github.com 443
	$ telnet packagecloud.io 443
	3- İnstall prerequisite erlang package with command below.
	$ yum install erlang
	
	* if you are working with local repos, you have to download erlang rpm package before 'yum install' step.
	   $ sudo yum install epel-release
   $ wget https://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
   $ sudo rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
	   $ yum install erlang
	
	4- First we'll update our yum repos.
	$ yum -y update
	
	5- clone git repo for necessary script.
	
	$ git clone https://github.com/ayhangulbjk/forrabbitmq.git
	Cloning into 'forrabbitmq'...
	remote: Enumerating objects: 6, done.
	remote: Counting objects: 100% (6/6), done.
	remote: Compressing objects: 100% (4/4), done.
	remote: Total 6 (delta 0), reused 6 (delta 0), pack-reused 0
	Receiving objects: 100% (6/6), done.
	
	*** with this script we can easyly download and configure repository information for OS that we want to install rabbitmq.
	
	6- Run shell script.
	$ cd forrabbitmq/
	$ sh script.rpm.sh
	Detected operating system as rhel/7.
	Checking for curl...
	Detected curl...
	Downloading repository file: https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/config_file.repo?os=rhel&dist=7&source=script
	done.
	Installing pygpgme to verify GPG signatures…
	
	See this at the end of output: " The repository is setup! You can now install packages."
	
	** installed repository destination: file:///etc/yum.repos.d/rabbitmq_rabbitmq-server.repo
	*** Please check repository file before go further. 
	        İt has to be something like this:
	$ vi /etc/yum.repos.d/rabbitmq_rabbitmq-server.repo
	[rabbitmq_rabbitmq-server]
	name=rabbitmq_rabbitmq-server
	baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/$basearch
	gpgcheck=1
	enabled=0
	
	7- Once you have configured repository, install rabbitmq server on RHEL / CentOS 7-8 by running below commands.
	$ yum makecache -y --disablerepo='*' --enablerepo='rabbitmq_rabbitmq-server' 
	$ yum -y install rabbitmq-server
	
	8- See package details with command below:
	$ rpm -qi rabbitmq-server 
	Name        : rabbitmq-server
	Version     : 3.3.5
	Release     : 34.el7
	Architecture: noarch
	Install Date: Wed 23 Feb 2022 10:42:06 AM +03
	Group       : Development/Libraries
	Size        : 5044476
	License     : MPLv1.1
	Signature   : RSA/SHA256, Thu 23 Mar 2017 07:38:33 PM +03, Key ID 6a2faea2352c64e5
	Source RPM  : rabbitmq-server-3.3.5-34.el7.src.rpm
	Build Date  : Thu 23 Mar 2017 07:14:19 PM +03
	Build Host  : buildhw-03.phx2.fedoraproject.org
	Relocations : (not relocatable)
	Packager    : Fedora Project
	Vendor      : Fedora Project
	URL         : http://www.rabbitmq.com/
	Summary     : The RabbitMQ server
	Description :
	RabbitMQ is an implementation of AMQP, the emerging standard for high
	performance enterprise messaging. The RabbitMQ server is a robust and
	scalable implementation of an AMQP broker.
	
	9- Start service:
	$ systemctl enable --now rabbitmq-server.service
	10- See service status:
	$ systemctl status rabbitmq-server.service 
	● rabbitmq-server.service - RabbitMQ broker
	   Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: disabled)
	   Active: active (running) since Fri 2022-02-25 10:54:51 +03; 2h 13min ago
	  Process: 15575 ExecStop=/usr/lib/rabbitmq/bin/rabbitmqctl stop (code=exited, status=0/SUCCESS)
	 Main PID: 15633 (beam.smp)
	   CGroup: /system.slice/rabbitmq-server.service
	           ├─15633 /usr/lib64/erlang/erts-5.10.4/bin/beam.smp -W w -K true -A30 -P 1048576 -- -root /usr/lib64/erlang -progname erl -- -home /var/lib/rabbitmq -- -pa ...
	           ├─15648 /usr/lib64/erlang/erts-5.10.4/bin/epmd -daemon
	           ├─15732 inet_gethost 4
	           └─15733 inet_gethost 4
	
	Feb 25 10:54:49 galadriel02 systemd[1]: Got notification message from PID 15679, but reception only permitted for main PID 15633
	Feb 25 10:54:49 galadriel02 systemd[1]: Got notification message from PID 15680, but reception only permitted for main PID 15633
	
	11- See internal detail of rabbitmq service:
	$ rabbitmqctl status
	Status of node rabbit@servername...
	[{pid,15633},
	 {running_applications,
	     [{rabbitmq_management,"RabbitMQ Management Console","3.3.5"},
	      {rabbitmq_web_dispatch,"RabbitMQ Web Dispatcher","3.3.5"},
	 {listeners,[{clustering,25672,"::"},{amqp,5672,"::"}]},
	 {vm_memory_high_watermark,0.4},
	 {vm_memory_limit,6658881945},
	 {disk_free_limit,50000000},
	 {disk_free,31176589312}, …
	
	12- Enable rabbitmq management dashboard:
	$ systemctl status rabbitmq-server.service
	Enabling plugins on node rabbit@servername:
	 rabbitmq_management
	 The following plugins have been configured:
	   rabbitmq_management
	   rabbitmq_management_agent
	   rabbitmq_web_dispatch
	 Applying plugin configuration to rabbit@rhel8…
	 The following plugins have been enabled:
	   rabbitmq_management
	   rabbitmq_management_agent
	   rabbitmq_web_dispatch
	 started 3 plugins.
	
	13- Create user for management console:
	$ rabbitmqctl add_user admin welcome
	$ rabbitmqctl set_user_tags admin administrator
	$ rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
	$ rabbitmqctl status
	
	14- it's important to restart service after enablingthe management console with:
	$ service rabbitmq-server restart
	
	15- Check for if listening:
	$ ss -tunelp | grep 15672
	tcp    LISTEN     0      128       *:15672                 *:*                   users:(("beam.smp",pid=15633,fd=17)) uid:774 ino:6655754 sk:ffff9b3d2d5b1f00 <->
	
	16- Copy rabbitmqadmin to /usr/local/bin/ and give execute permission for this feature.
	$ cp -rf  rabbitmqadmin /usr/local/bin/
	$ chmod +x /usr/local/bin/rabbitmqadmin
	$ sh -c 'rabbitmqadmin --bash-completion > /etc/bash_completion.d/rabbitmqadmin' 
	
	17- Open management dashboard at: http://localhost:15672/
	
	
	
	From now on amqp is listening at port 5672.
	And management console is listening  at port 15672.
	
	Example for publishing a message with python:
	1- İnstall pika package for connecting to the amqp.
	$ pip3 install pika
	
	if your server has restricted  internet access and not connecting to pythonhosted.org please try download whl file  on https://pypi.org/project/pika/
	and do the following:
	$ pip3 install pika-1.2.0-py2.py3-none-any.whl
	Processing ./pika-1.2.0-py2.py3-none-any.whl
	Installing collected packages: pika
	Successfully installed pika-1.2.0
	
	2- Create publisher.py file with code below.
	
	#!/usr/bin/env python
	import pika
	
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='10.220.13.31'))
	channel = connection.channel()
	channel.queue_declare(queue='firstqueue')
	channel.basic_publish(exchange='', routing_key='firstqueue', body='Hello, this is first message!')
	print(" [x] Sent 'Hello, this is first message!''")
	connection.close()
	
	3- Run file.
	
	$python3 publisher.py
	 [x] Sent 'Hello, this is first message!''
	After first message:
	
	
	
	
	
	
	Example for consuming message with python:
	1- Create consumer.py file with code below.
	#!/usr/bin/env python
	import pika, sys, os
	
	
	def main():
	    connection = pika.BlockingConnection(pika.ConnectionParameters(host="10.220.13.31"))
	    channel = connection.channel()
	    channel.queue_declare(queue="firstqueue")
	
	    def callback(ch, method, properties, body):
	        print(" [x] Received %r" % body)
	
	    channel.basic_consume(
	        queue="firstqueue", on_message_callback=callback, auto_ack=True
	    )
	    print(" [*] Waiting for messages. To exit press CTRL C")
	    channel.start_consuming()
	
	
	if __name__ == "__main__":
	    try:
	        main()
	    except KeyboardInterrupt:
	        print("Interrupted")
	        try:
	            sys.exit(0)
	        except SystemExit:
	            os._exit(0)

	2- Run file.
	$python3 consumer.py
	 [*] Waiting for messages. To exit press CTRL C
	 [x] Received b'Hello, this is first message!'
	
	3- After consuming the message on the queue, the message on ready status returned to 0. Because out consumer code contains parameter auto_ack=True
	
