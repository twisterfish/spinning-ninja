# Spinning Ninja Website
This is a basic site for spinning ninja

## Using AWS S3
Pros
1. cheap, way cheap
2. minimal knowledge required to update
3. complete customization available
4. Access to a relational database for queries if needed (MySQL)
5. stable company
Cons
1. No WYSIWYG editor available in console

# Using Hosting Service
Pros
1. Most have a WYSIWYG editor available
2. Easy to maintain UI portions
Cons
1. Rigid guardrails in functionality
2. Database access may not be available
3. Data imports and exports may be difficult or nonexistant
4. Dificult learning curve when going outside the template
5. Customization may be more complex than necessary
6. Some providers are sketch
7. Most of them host on AWS anyway

# Methods to Update
1. convert plists to csv and upload to site
2. upload plists and use a lambda function to convert in place
3. import csv into a relational database (MySQL) and render dynamic html
4. upload plist into a bucket and kickoff Lambda to generate html
  
## dynamic Lambda function code

#######################################################################
# def lambda_handler(event, context):
#     print(event)
#     return 'Notes to convert this to a Lambda function!'
#######################################################################