** **

## Deduplicating-Cloud-functions 

Deduplication is useful for organizations dealing with highly redundant operations that requires constant copying and storing of data for future reference or recovery purpose. 

The term is explained as an approach that eliminates duplicate copies of data from the system. For instance, a file that is backed up every week results in a lot of duplicate data and thus, eats up considerable disk space. Deduplication run an analysis and eliminates these sets of duplicate data and keeps only what is unique and essential, thus significantly clearing storage space. Here are some benefits of data deduplication for organizations.

  * Clears storage space: Running the technique can help reduce storage requirements by up to 80% for backups and files. This allows         organizations save far more data on the same system and extends disk purchase intervals automatically. With the advantage of speed,     organizations can store data to disk cost effectively.

  * Adept replication: The deduplication process writes only unique data on the disk and thus, there’s need to replicate only these set     of blocks. Depending on the type of application, the traffic for data replication can be reduced by 90%.

  * Effective use of network bandwidth: If data deduplication takes place at sources, there’s no need to transmit data over the network,     thus eliminating unwanted use of network bandwidth.

  * Cost-effective: As fewer disks are required, storage cost is reduced significantly. Besides, it also tends to improve disaster           recovery as lesser amount of data is transferred.

With the massive data explosion, technologies that offers approaches to efficiently manage it is considered real attractive.Deduplication is one such technology that assist with effectively managing storage devices as it enables efficient usage of data storage and network bandwidth.

The purpose of this project is to design and implement a novel storage de-duplication framework for serverless platform in order to improve overall throughput of the platform.

** **

## 1.   Vision and Goals Of The Project:

The final product of this project will be a de-duplication service that leverages application-aware semantic-equivalence to identify duplicate data at storage system and avoids redundant invocation of functions on servers. Main goals include:

  * Define and implement specialized data curation techniques
  * Optimize de-duplication data structure and indexing
  * Perform data and event de-duplication to avoid redundant execution of stateless functions
  * Demonstrate the efficiency in performing function deduplication by deduplicating data
  

## 2. Users/Personas Of The Project:

**It does not target:**

   * MOC admin users, who will work against the command line.
   * Administrators of cloud services, who will continue to use the services of serverless functions.

**It targets:**

   * Cloud vendors who design their serverless build environement. This will execute stateless functions without worrying internal            details as it saves them money by saving the functions calls in an instance.
   * Virtual desktop infrastructure (VDI) is another very good candidate for deduplication, because the duplicate data among desktops is      very high

** **

## 3.   Scope and Features Of The Project:

**What will be delivered?**

* Presents a faster framework for cloud providers: 

  * For providers who mostly deal with data generated from external end-points like IoT devices, cloud systems monitors, weather sensors, social media, mobile devices, etc

  * By avoiding container startup latency: Since most platforms execute stateless functions inside containers, eliminating redundant activation of functions results in low latency.

*  Presents a framework for improving “performance/cost” for end-users: 

    * End-users will use this framework indirectly which will, in turn, decrease the application cost for them since this framework increases throughput.

    * Availability to improve throughput by offering the user to define PoVs: PoVs(Point of Variability) are parts of the data that is not important for the execution and should be ignored such as metadata. Availability of letting the user choose those points allows a more fine-grained de-duplication.

* Scalability: This novel storage de-duplication framework is designed and will be implemented for serverless execution model which in principle is flexible regarding scaling. An application can be scaled automatically or by adjusting its capacity through toggling the units of consumption.

* Security: Security can be ensured by writing secure application code and tight access control over source code. 

**What will not be delivered?**

* This framework does not help save storage space since for every new data coming original data is stored multiple times.(fix this or delete it)

* This system can only be implemented on storage closed-loop functions, which takes data from data storage and writes the result again to the data storage. However, external stimuli functions are not the part of this de-duplication design because they take their data from storage but then trigger external events.

** **

## 4. Solution Concept

### Background & Motivation

Serverless platforms mostly execute functions inside containers that are typically reused across multiple invocations of the same function to mask the container startup latency. However, state maintained locally by a function might not be available across invocations. In order to be scalable concerning the incoming events by design all serverless platforms implement stateless function semantics. These stateless functions can also be identified as idempotent which means they compute same result for duplicate data.

Serverless applications typically have data sources as IoT/sensor data, social media data, user activity data and system state monitoring data. Data generated from these sources are largely consistent, causing data duplication. For example, for the generic cases the boundaries for temperature is very tight and the degree value is mostly consistent for a specific location of the sensor. In this case, our system will be getting extensive amount of duplicate data during the day.

In the light of the above facts and the distributed storage and server architecture in serverless systems, an opportunity arises to build a specialized data de-duplication service which will de-duplicate the cloud function invocations.

### Global Architectural Structure Of the Project:

Ideally, we would implement such deduplication inside existing open serverless framework like [OpenWhisk](https://openwhisk.apache.org/), but given time constraint we will implement a POC, where we will build these dedup components *on-top of* OpenWhisk instead of inside OpenWhisk. So essentially, users now will interact with our layer instead of interacting with OpenWhisk directly.

 1. Users will register their data sources (IoT, System logs, etc.) to our service (sanity)
 2. Users will register their functions that they want to execute for their data events
 
 Currently our framework supports multi-user.
 
 Components of Sanity Framework: 
 
 * **Cloud Object Store** : [Minio](https://min.io/)
 * **Message/Event Buffer**: [Kafka](https://kafka.apache.org/)
 * **Database** : [CouchDB](http://couchdb.apache.org/) 
 * **Serverless Platform**: [Openwhisk](https://openwhisk.apache.org/)
 * **Sanity controller**

### De-duplicating architecture 

Function Types
There are two types of functions in Serverless: Storage closed loop and External Stimuli. External stimuli functions get their input from data store then create external events whereas storage closed loop functions get their input from storage and also write their result to storage. The latter one is our main concern in this project.

|![alt text](https://github.com/bu-528-sp19/Deduplicating-Cloud-functions/blob/master/images/functiontypes.JPG)|
|:--:| 
| *Figure 1: Function Types in Serverless* |


|![alt text](https://github.com/bu-528-sp19/Deduplicating-Cloud-functions/blob/master/images/architecture_diagram_1.PNG)|
|:--:| 
| *Figure 2: Overall Architecture* |


### Pipleline of the reference architecture

In our architecture, Sanity controller will be the brain of the design. It will be in communication with other components. 

A user can define functions on wsk client:
```
wsk -i action create myfunction.py myfunction
```
Upload a file to a Minio bucket:
```
mc cp <input_file> myminio/<input_bucket>
```
Invoke the function with the uploaded file as an input and store the result in output_bucket:
```
wsk -i action invoke myfunction <input_bucket>/<input_file> <output_bucket>
```
In Sanity, each user has their own database document in CouchDB that is hold seperately. Sanity, currently supports multi-user. When a user comes, Sanity first checks if the user already exists in the framework by checking a special DB created in couchDB. If the user is a new user, that user is registered to our framework and assigned a database document. In that document also every function has their own inputs registered. Previously provided inputs for a specific function are registered in database under that function for deduplicating purposes. That is, in a sample user document shown in figure 3, there are two functions registered for that user: "testfunc_1" and "testfunc_2". Those two functions has two different input data registered each such as "testfunc_1" has "testdata_1a" and "testdata_1b" as its previously used inputs and similarly "testfunc_2" has "testdata_2a" and "testdata_2b" as its previously used inputs. The values of these input data which are shown empty in figure would be the inio bucket reference locations of the results when executed with that specific function. For example, let's say the user executed "testfunc_1" with "testdata_1a" as the input and the result is recorded to "func1_outbucket" and the name of the resulting output file is "outdata_1a". In that case the CouchDB schema will look like this:

```JSON
"testfunc_1" : {
     "testdata_1a" : "func1_outbucket/outdata_1a"
}
```

|![alt text](https://github.com/bu-528-sp19/Deduplicating-Cloud-functions/blob/master/couchdb_user_schema.PNG)|
|:--:| 
| *Figure 3: CouchDB - Sample User Document* |

Examples above used real names of functions and data however, these are used for simplicity. In our framework we use hashes of functions and data to determine uniqueness. Note that, this way even if two equal functions/data with different names comes to our framework, Sanity is able to detect those functions/data are same by comparing hashes and de-duplicate accordingly.

_When unique data comes;_

Incoming data is recorded in a minio bucket. Kafka captures this event and streams for further processing. Sanity Controller gets the necessary info from Kafka stream. Controller cross-checks the checksum of the incoming data/function for the online user with CouchDB. Controller decides that the data is unique (i.e. never used before). Then, controller send invokes Openwhisk function to execute with the unique data. Openwhisk runs the function and generates an output. The output reference (bucket and file name) is saved to CouchDB as the value of the unique data. This process is shown in figure 4 with blue arrows.

_When duplicate data comes;_

Controller cross-checks the checksum of the incoming data/function for the online user with CouchDB. Controller decides that the data is duplicate (i.e. used before). Then, controller gets the location information of the output data from CouchDB and get the output from related minio bucket in oreder to provide to the user. This process is shown in figure 4 with red arrows.

|![alt text](https://github.com/bu-528-sp19/Deduplicating-Cloud-functions/blob/master/final_arch.PNG)|
|:--:| 
| *Figure 4: Our Architecture* |


## CLI: How a user can run functions on Sanity

sanity --i  <input_bucket> --o <output_bucket>  --f   <function_name>

## [Our project video](add link)

## 5. Acceptance criteria

Minimum acceptance criteria are:

  * To prevent data duplication which in turn would prevent event duplication.
  * Implement different usecases for the same
  * The architecture should able to cater different usecases (Generalizing the architecture)
  * User should interact with the framework through CLI

Minimum acceptance criteria is currently achieved.

## 6. Future Steps:

  * Implement multi-thread to Sanity
  * Improve user authentication
   * Currently, the system is not password protected, support will be added.
  * Benchmark the whole framework and write an academic article according to the results
  * Generalize sanity to support multiple serverless platforms

## 6.  Release Planning:

Sprint 1(Due to 2.14): 
  * Familiarize ourselves with Serverless Technology
  * Get detail understanding on the internal working of the standard open serverless framework, viz. [OpenWhisk](https://openwhisk.apache.org/)
  * Learn about storage deduplication techniques
  * Read literature/papers on existing deduplication techniques addressing similar problems
  
Sprint 2(Due to 2.28):
  * Set up Kafka, Minio and other relevant features by implementing a use case.
  * Start working towards Sanity Controller
  
Sprint 3(Due to 3.21):
  * Developing the de duplication framework, sanity controller
  * Implement a use case (Image Thumbnail) to test the de duplication
  
Sprint 4(Due to 4.04):
  * Generalizing the sanity architecture for handling any kind of incoming data for deduplication
  * Benchmarking the current architecture on performing different use cases with and without sanity controller
  * Designing the CLI, using which User can interact with the sanity controller

Sprint 5(Due to 4.18):
  * Integrating CLI with the architecture
  * Evaluate performance savings of the system on different dimensions:
  * Savings in avoiding function (container) invocations
    * Savings in time to execute the function 
    * Savings in time accessing duplicate data from COS

## References

 * What is Data deduplication and it's uses: 
 (http://blog.webwerks.in/cloud-hosting-blog/what-are-the-real-benefits-of-data-deduplication-in-cloud)
 * Sanity: The Less Server Architecture for Cloud functions(http://niltonbila.com/pub/Nadgowda-WoSC17.pdf)

