# Write Up for Try Hack Me box - [Joker](https://tryhackme.com/room/jokerctf)

The initial access is joomla CMS.\
The next stage is lxc grouip priv esc.

> Pratyush Prakhar (5#1NC#4N) - 02/11/2024

## RECONNAISSANCE

1. It is RUSTscan time.
	1. Full port scan --> [nmap file here](rustscan/all.nmap).

	**Results**

	```bash
	└─$ rustscan --range 1-65535 -a 10.10.223.63 -- -sC -sV -oN rustscan/all.nmap
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: https://discord.gg/GFrQsGy           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	Please contribute more quotes to our GitHub https://github.com/rustscan/rustscan

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.223.63:22
	Open 10.10.223.63:80
	Open 10.10.223.63:8080
	[~] Starting Script(s)
	[>] Script to be run Some("nmap -vvv -p {{port}} {{ip}}")

	[~] Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-02-12 17:27 EST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	Initiating Ping Scan at 17:27
	Scanning 10.10.223.63 [2 ports]
	Completed Ping Scan at 17:27, 0.21s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 17:27
	Completed Parallel DNS resolution of 1 host. at 17:27, 0.02s elapsed
	DNS resolution of 1 IPs took 0.02s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 17:27
	Scanning 10.10.223.63 [3 ports]
	Discovered open port 8080/tcp on 10.10.223.63
	Discovered open port 22/tcp on 10.10.223.63
	Discovered open port 80/tcp on 10.10.223.63
	Completed Connect Scan at 17:27, 0.20s elapsed (3 total ports)
	Initiating Service scan at 17:27
	Scanning 3 services on 10.10.223.63
	Completed Service scan at 17:27, 6.45s elapsed (3 services on 1 host)
	NSE: Script scanning 10.10.223.63.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 6.67s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.91s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	Nmap scan report for 10.10.223.63
	Host is up, received syn-ack (0.21s latency).
	Scanned at 2024-02-12 17:27:07 EST for 14s

	PORT     STATE SERVICE REASON  VERSION
	22/tcp   open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 ad:20:1f:f4:33:1b:00:70:b3:85:cb:87:00:c4:f4:f7 (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDL89x6yGLD8uQ9HgFK1nvBGpjT6KJXIwZZ56/pjgdRK/dOSpvl0ckMaa68V9bLHvn0Oerh2oa4Q5yCnwddrQnm7JHJ4gNAM+lg+ML7+cIULAHqXFKPpPAjvEWJ7T6+NRrLc9q8EixBsbEPuNer4tGGyUJXg6GpjWL5jZ79TwZ80ANcYPVGPZbrcCfx5yR/1KBTcpEdUsounHjpnpDS/i+2rJ3ua8IPUrqcY3GzlDcvF7d/+oO9GxQ0wjpy1po6lDJ/LytU6IPFZ1Gn/xpRsOxw0N35S7fDuhn69XlXj8xiDDbTlOhD4sNxckX0veXKpo6ynQh5t3yM5CxAQdqRKgFF
	|   256 1b:f9:a8:ec:fd:35:ec:fb:04:d5:ee:2a:a1:7a:4f:78 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOzF9YUxQxzgUVsmwq9ZtROK9XiPOB0quHBIwbMQPScfnLbF3/Fws+Ffm/l0NV7aIua0W7FLGP3U4cxZEDFIzfQ=
	|   256 dc:d7:dd:6e:f6:71:1f:8c:2c:2c:a1:34:6d:29:99:20 (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPLWfYB8/GSsvhS7b9c6hpXJCO6p1RvLsv4RJMvN4B3r
	80/tcp   open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
	| http-methods: 
	|_  Supported Methods: GET POST OPTIONS HEAD
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	|_http-title: HA: Joker
	8080/tcp open  http    syn-ack Apache httpd 2.4.29
	|_http-title: 401 Unauthorized
	| http-auth: 
	| HTTP/1.1 401 Unauthorized\x0D
	|_  Basic realm=Please enter the password.
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:27
	Completed NSE at 17:27, 0.00s elapsed
	```

	2. Full Service and Scripts scan on the found ports. --> [nmap file here](rustscan/main.nmap))

	**Results**

	```bash
	└─$ rustscan -a 10.10.223.63 -- -sC -sV -oN rustscan/main.nmap
	.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
	| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
	| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
	`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
	The Modern Day Port Scanner.
	________________________________________
	: https://discord.gg/GFrQsGy           :
	: https://github.com/RustScan/RustScan :
	--------------------------------------
	🌍HACK THE PLANET🌍

	[~] The config file is expected to be at "/home/kali/.rustscan.toml"
	[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
	[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
	Open 10.10.223.63:22
	Open 10.10.223.63:80
	Open 10.10.223.63:8080
	[~] Starting Script(s)
	[>] Script to be run Some("nmap -vvv -p {{port}} {{ip}}")

	[~] Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-02-12 17:24 EST
	NSE: Loaded 156 scripts for scanning.
	NSE: Script Pre-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:24
	Completed NSE at 17:24, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:24
	Completed NSE at 17:24, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:24
	Completed NSE at 17:24, 0.00s elapsed
	Initiating Ping Scan at 17:24
	Scanning 10.10.223.63 [2 ports]
	Completed Ping Scan at 17:24, 0.21s elapsed (1 total hosts)
	Initiating Parallel DNS resolution of 1 host. at 17:24
	Completed Parallel DNS resolution of 1 host. at 17:24, 0.01s elapsed
	DNS resolution of 1 IPs took 0.01s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
	Initiating Connect Scan at 17:24
	Scanning 10.10.223.63 [3 ports]
	Discovered open port 80/tcp on 10.10.223.63
	Discovered open port 22/tcp on 10.10.223.63
	Discovered open port 8080/tcp on 10.10.223.63
	Completed Connect Scan at 17:24, 0.20s elapsed (3 total ports)
	Initiating Service scan at 17:24
	Scanning 3 services on 10.10.223.63
	Completed Service scan at 17:24, 6.57s elapsed (3 services on 1 host)
	NSE: Script scanning 10.10.223.63.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:24
	Completed NSE at 17:25, 7.04s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:25
	Completed NSE at 17:25, 0.89s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:25
	Completed NSE at 17:25, 0.00s elapsed
	Nmap scan report for 10.10.223.63
	Host is up, received syn-ack (0.21s latency).
	Scanned at 2024-02-12 17:24:48 EST for 15s

	PORT     STATE SERVICE REASON  VERSION
	22/tcp   open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 ad:20:1f:f4:33:1b:00:70:b3:85:cb:87:00:c4:f4:f7 (RSA)
	| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDL89x6yGLD8uQ9HgFK1nvBGpjT6KJXIwZZ56/pjgdRK/dOSpvl0ckMaa68V9bLHvn0Oerh2oa4Q5yCnwddrQnm7JHJ4gNAM+lg+ML7+cIULAHqXFKPpPAjvEWJ7T6+NRrLc9q8EixBsbEPuNer4tGGyUJXg6GpjWL5jZ79TwZ80ANcYPVGPZbrcCfx5yR/1KBTcpEdUsounHjpnpDS/i+2rJ3ua8IPUrqcY3GzlDcvF7d/+oO9GxQ0wjpy1po6lDJ/LytU6IPFZ1Gn/xpRsOxw0N35S7fDuhn69XlXj8xiDDbTlOhD4sNxckX0veXKpo6ynQh5t3yM5CxAQdqRKgFF
	|   256 1b:f9:a8:ec:fd:35:ec:fb:04:d5:ee:2a:a1:7a:4f:78 (ECDSA)
	| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOzF9YUxQxzgUVsmwq9ZtROK9XiPOB0quHBIwbMQPScfnLbF3/Fws+Ffm/l0NV7aIua0W7FLGP3U4cxZEDFIzfQ=
	|   256 dc:d7:dd:6e:f6:71:1f:8c:2c:2c:a1:34:6d:29:99:20 (ED25519)
	|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPLWfYB8/GSsvhS7b9c6hpXJCO6p1RvLsv4RJMvN4B3r
	80/tcp   open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
	|_http-title: HA: Joker
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	| http-methods: 
	|_  Supported Methods: GET POST OPTIONS HEAD
	8080/tcp open  http    syn-ack Apache httpd 2.4.29
	| http-auth: 
	| HTTP/1.1 401 Unauthorized\x0D
	|_  Basic realm=Please enter the password.
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	|_http-title: 401 Unauthorized
	Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel

	NSE: Script Post-scanning.
	NSE: Starting runlevel 1 (of 3) scan.
	Initiating NSE at 17:25
	Completed NSE at 17:25, 0.00s elapsed
	NSE: Starting runlevel 2 (of 3) scan.
	Initiating NSE at 17:25
	Completed NSE at 17:25, 0.00s elapsed
	NSE: Starting runlevel 3 (of 3) scan.
	Initiating NSE at 17:25
	Completed NSE at 17:25, 0.00s elapsed
	```

2. There are **3 TCP** ports open. 
	1. *Port 22* - SSH - **OpenSSH 7.6p1** 
	2. *Port 80* - WEB - **Apache httpd 2.4.29**
	3. *Port 8080* - WEB - **Apache httpd 2.4.29**

3. Let's explore WEB part first. Then we can use SSH.


## WEB

1. Let's first check out the web server on port 80. 
	1. We get a default page with no links going out. - Default HTML page.
	\
	![](images/port-80.png)

	2. We will go for the low hanging fruit - robots, page source and try to get some information. Interesting thing found were two usernames - `batman` and `joker`. Also, the backend processes php.
	\
	![](images/secret.png)
	\
	\
	![](images/phpinfo.png)
	
	3. Here is the dirb [file](web/dirb/ferox-80.txt) for the reference.

2. Nothing else interesting here, let's move to web page at 8080. But it is protected by a `Basic Digest`. Let's try to brute force it with our known users as this is a weak cryptography method.
	1. Ran a fuzzer for the Basic digest using hydra. We got a match here - [joker pass](web/joker_pass.txt)
	2. Let's keep of track of it as we are .... forgetful. [FILE](creds.txt)
\
![](images/port-8080.png)
\

3. We get into the the web server on port 8080.
	1. Checking for the basic things, we find we are on a  `Joomla Server`.
	2. We can explore more by dirbusting. through this we find the admin page.
	3.But we do't have any viable creds for the login. So, let's go and find some.
	\
	![](images/port-8080-robots.png)

4. We found a `backup.zip` earlier. Let's explore that. 
	1. We find that it is a backup of a older system directories. It has a SQL file on it that might contain some useful information. 
	2. On looking through the [file](web/backup/db/joomladb.sql), we find a user - `Super Duper User` with a [password](web/admin_pass.txt).
	3. We can use some tools as **hashid**, **hash-identifier**, **hashcat** and **john** to find the right password here - [cracked pass](web/admin_crack_pass.txt). Again logged [here](creds.txt).

5. Luckily, we see that the admin is stupid enough to reuse password. We can login into the Joomla dashboard. 
\
![alt text](images/joomla-admin.png)
\

6. Let's use this articles help to get our initial access through `template misuse` - https://www.hackingarticles.in/joomla-reverse-shell/.


## INITIAL ACCESS - REV SHELL

1. We get into the system as `www-data`. We can go around to check for low hanging fruits but can also take help of out linpeas.

2. We see from our [scan](ssh/tmp/linpeas_www.out) that our user is part of a `lxd` group. We know that exec pretty well. Here is the reference [article](https://www.hackingarticles.in/lxd-privilege-escalation/).

3. We develop a alpine image mentioned [here](ssh/www-data/lxd-alpine-builder/alpine-v3.13-x86_64-20210218_0139.tar.gz).

## PRIVESC

1. We can put the image on our victim and exploit the LXD path. We get the final file by reading the root directory.

```bash
www-data@ubuntu:/mnt$ cd -                     
/tmp
www-data@ubuntu:/tmp$ lxc exec ignite /bin/sh  
~ # whoami
root
~ # bash
/bin/sh: bash: not found
~ # /bin/bash
/bin/sh: /bin/bash: not found
~ # ls
~ # cd mnt/root/root
/bin/sh: cd: can't cd to mnt/root/root: No such file or directory
~ # cd /mnt/root/
/mnt/root # ls
bin             initrd.img      media           run             tmp
boot            initrd.img.old  mnt             sbin            usr
dev             lib             opt             srv             var
etc             lib64           proc            swapfile        vmlinuz
home            lost+found      root            sys             vmlinuz.old
/mnt/root # cd root
/mnt/root/root # ls
final.txt
/mnt/root/root # cat final.txt 

     ██╗ ██████╗ ██╗  ██╗███████╗██████╗ 
     ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
     ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                         
!! Congrats you have finished this task !!

Contact us here:

Hacking Articles : https://twitter.com/rajchandel/
Aarti Singh: https://in.linkedin.com/in/aarti-singh-353698114

+-+-+-+-+-+ +-+-+-+-+-+-+-+
 |E|n|j|o|y| |H|A|C|K|I|N|G|
 +-+-+-+-+-+ +-+-+-+-+-+-+-+
```

2. I leave you with a thought - Do you want to know how I got these scars?....

## BROWNIE POINTS

1. What version of Apache is it? - **2.4.29**

2. What port on this machine not need to be authenticated by user and password? - **80**

3. There is a file on this port that seems to be secret, what is it? - **secret.txt**

4. There is another file which reveals information of the backend, what is it? - **phpinfo.php**

5. When reading the secret file, We find with a conversation that seems contains at least two users and some keywords that can be intersting, what user do you think it is? - **joker**

6. What port on this machine need to be authenticated by Basic Authentication Mechanism? - **8080**

7. At this point we have one user and a url that needs to be aunthenticated, brute force it to get the password, what is that password? - **hannah**

8. Yeah!! We got the user and password and we see a cms based blog. Now check for directories and files in this port. What directory looks like as admin directory? - **/administrator/**

9. We need access to the administration of the site in order to get a shell, there is a backup file, What is this file? - **backup.zip**

10. We have the backup file and now we should look for some information, for example database, configuration files, etc ... But the backup file seems to be encrypted. What is the password? - **hannah**

11. In our new discovery we see some files that have compromising information, maybe db? ok what if we do a restoration of the database! Some tables must have something like user_table! What is the super duper user? - **admin**

12. Super Duper User! What is the password? - **abcd1234**

13. At this point, you should be upload a reverse-shell in order to gain shell access. What is the owner of this session? - **www-data**

14. This user belongs to a group that differs on your own group, What is this group? - **lxd**

15. What is the name of the file in the /root directory? - **final.txt**

**Stay Tuned On**\
[GitHub](https://github.com/pratty010/Boxes)\
[LinkedIn](https://www.linkedin.com/in/pratyush-prakhar/)