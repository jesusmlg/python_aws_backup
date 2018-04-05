<?php

    require 'vendor/autoload.php';
    use Aws\Ec2\Ec2Client;

    $ec2Client = new Ec2Client([
        'version' => 'latest',
        'region'  => 'eu-west-1',
        
    ]);
    $instances = $ec2Client->describeInstances(['filters'=>[ 'Owners' => 'self'

    ]]);
    

    var_dump($instances['Reservations'][3]['Instances'][0]['Tags']);
    //echo count($instances['Reservations'][3]['Instances']);

    
?>