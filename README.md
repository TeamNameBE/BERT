# BERT

a Bot Excelling in Reminding Things


## Supported Commands

* **/addreminder** date(jj/mm/yyy) hour(HH:MM) name(no space) duration(HH:MM) peopletoremind(@role)
  * creates a reminder at the given date that concerns the mentionned role/user
* **/delreminder** name
  * deletes a reminder
* **/modreminder** name parameter(name|start_date|duration|channel|allow_dp) new_value
  * Modifies the given field of a reminder
* **/getfuture** [hours|days|weeks] value
  * Returns the reminders until the given date (defaults to next week)
* **/help** [command]
  * displays help message about the specified command, or about every command
* **/deathping** [@someone]
  * Deathping someone (May be multiple people)
* **/stopping** [@someone]
  * Stops a deathping on someone
* **/morsty**
  * ? ? ?
* **/vote** "Question" "proposition0" ... "proposition10"
  * Creates an embed message for a quick vote

## Installation

```
virtualenv -p python3 ve/
source ve/bin/activate
pip install -r requirements.txt
```
