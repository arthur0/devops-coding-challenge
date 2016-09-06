#Description

Describe the APP what it does, the basic endpoints, expectation of traffic.

### App Architecture
* Flask Server
* Workers Machines
* Redis Server 
* MongoDB

### Endpoints

/xxx/
/yyy/

#### Running Tests

XXX

Please note that Part 1 is independente of Part 2.

Please fork this repo and send the link for it once the exercise is completed. Make sure you keep all code, documentation and instructions to deploy your solution.

## Part 1

Describe the deployment architecture and how you would implement it. Please mention what measure would you take for.

* Security
* Scalability
* Logging
* Monitoring
* Automation


## Part 2

For this part you need to request ssh for a machine. Please do that before we start.

### 2.1 Deployment
Write the necessary scripts for deployment for this APP. Note this can be a single machine deployment, no concerns with scalability are necessary. You should do so using Ansible and Fabric. If you have no experience with these tools but have experience with equivalent ones, please use the other tools.

### 2.2 Continous Integration
Set up a continuous integration system that runs the project tests after each commit and displaying on github the status of the build (Preferably use Jenkins).

### 2.3 Debuging
Endpoint /zzz/ has a bug. Tell us exactly what the problem is, and for extra credit try to fix it.    


