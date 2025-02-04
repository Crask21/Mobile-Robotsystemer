o
    �Hc�	  �                   @   sX   d dl m  mZ d dlZd dlmZ d dlZd dlZd dlZd dl	Z	G dd� d�Z
dS )�    N)�sleepc                   @   sT   e Zd Zddd�Zdd� Zdd� Zd	d
� Zddd�Zddd�Zddd�Z	dd� Z
dS )�bot�returnNc                 C   s\   t �� | _| j| j_| j| j_| j| j_| j�d� | j��  t�	t
j�| _d| _d| _d S )NZ	localhost�        )�mqttZClient�client�
on_connect�
on_message�on_disconnectZconnectZ
loop_start�termiosZ	tcgetattr�sys�stdin�settingsZlin_velZang_vel)�self� r   �nc:\Users\Markus Simonsen\Desktop\UNI\Robtek\3. sem\Mobile-Robotsystems\Turtlebot\Turtlebot_Python\moveClass.py�__init__	   s   




zbot.__init__c                 C   s   t d�|�� d S )NzConnected with result code: {}��print�format)r   r   �userdata�flags�rcr   r   r   r      �   zbot.on_connectc                 C   s&   t d�|�� |dkrt d� d S d S )Nz!Disconnected with result code: {}r   z5Unexpected disconnection, might be a network error...r   )r   r   r   r   r   r   r   r
      s   �zbot.on_disconnectc                 C   s@   |j �d�}td�|j|�� |jdkrtd� d S td� d S )Nzutf-8z(Recieved message. Topic: {}, message: {}Ztest_sub_topiczCheck.zNot a topic to react on.)�payload�decoder   r   Ztopic)r   r   r   �msg�messager   r   r   r	      s
   
zbot.on_messager   �{�G�z�?c                 C   s@   |ddd�dd|d�d�}t �|�}| jjd|d� t|� d S �Nr   )�x�y�z)ZlinearZangularZcmd_vel)r   )�json�dumpsr   �publishr   )r   Zlin�ang�time�pub_msgr   r   r   �drive%   s   

�
z	bot.drivec                 C   s�   t |�}t |�}ttt|�d ��D ]}| �d|t|� d d� q| �dt|�d d d | t|� d� ttt|�d ��D ]}| �|t|� d dd� qA| �|d d | t|� � d S )N�-   r   g�������?g      �?�
   g�������?r   )�float�range�int�absr)   )r   r&   Zdist�ir   r   r   �move,   s   *"zbot.movec                 C   s   | � dd|� d S )Nr   )r)   )r   Zdelayr   r   r   �stop9   r   zbot.stopc                 C   sT   dddd�dddd�d�}t �|�}| jjd|d�}|��  t�tjtj	| j
� d S r   )r#   r$   r   r%   Zwait_for_publishr   Z	tcsetattrr   r   Z	TCSADRAINr   )r   r(   �infor   r   r   �__del__<   s   

�
zbot.__del__)r   N)r   r   r   )r   r   )r   )�__name__�
__module__�__qualname__r   r   r
   r	   r)   r1   r2   r4   r   r   r   r   r      s    

	

r   )Zpaho.mqtt.clientr   r   r#   r'   r   r   ZselectZttyr   r   r   r   r   r   �<module>   s
    