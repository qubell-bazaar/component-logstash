Logstash
===============
Install and configure Logstash indexer. ServiceCall for consumer creation

Version 1.0-43p
---------------

[![Install](https://raw.github.com/qubell-bazaar/component-skeleton/master/img/install.png)](https://express.tonomi.com/applications/upload?metadataUrl=https://raw.github.com/qubell-bazaar/component-logstash/1.0-43p/meta.yml)


Features
--------
  - Install and configure Logstash indexer
  - ServiceCall for consumer creation

Configurations
--------------
  Indexer
  -------
  - Logstash 1.3.3, Kibana 3 , CentOS 6.4 (us-east-1/ami-bf5021d6), AWS EC2 m1.small, root
  
  Consumer
  --------
  - Logstash 1.3.3 consumer independent from OS

Consumer example
---------------

### For the first launch Logstash indexer and add it as [service](http://docs.qubell.com/actions/services/contents.html) to your [environment](http://docs.qubell.com/concepts/environments.html) 
### After that add consumers via [ServiceCall](http://docs.qubell.com/actions/services/serviceCall.html) to Logstash service
### Add consumer on apache host

    workflow:
       type: workflow.Instance
       interfaces:
         ...
         ## This is interface complimentary for the same interface in Logstah service. This will allow to perform ServiceCall
         logger:
           install-consumer: send-command(list<string> target-hosts, string identity, list<string> log_target => string kibana-dashboard-url)
         ...
       required: [logger,...]
       configuration:
         configuration.workflows:
           launch: 
             steps:
               ...
               ## After Apache install send its logs in our Logstash
               ## For that goal execute ServiceCall. Provide a few parameters: target-hosts(hosts ips for consumer installation), identity(credentials for target_hosts), log_target(in format: path_to_log::log_type(log_type need for logstash  grok filters))
               - enable-logger:
                    action: logger.install-consumer
                    precedingPhases: [ install-apache ]
                    parameters:
                      commandCallTimeout: 20 minutes
                      target-hosts: "{$.signals.vm.ips}"
                      identity:  "{$.image.user}"
                      log_target: ["/var/log/httpd/error.log::apache-error", "/var/log/httpd/access.log::apache-access"]
                    output:
                     kibana-dashboard-url: kibana-dashboard-url
             return: ### Values returned from workflow
                ...
                ##  Url to Kibana dashboard with filter for that host
                kibana-dashboard-url:
                value: "{$.kibana-dashboard-url}"
