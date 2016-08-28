# Tweetcool

The message wall application for Codecoolers

## Server

The server script is used to serve the client applications.
It's purpose is to store the given tweets and send them back when requested.

Available requests:

### / GET
testing address: `/` (method: GET)
It returns the `It works!` string.

### /tweet GET
getting tweets: `/tweet` (method: GET)
optional parameters:

| Parameters | details                                                              | data type | default value |
|------------|----------------------------------------------------------------------|-----------|---------------|
| limit      | Number of results to return.                                         | int       | 10            |
| offset     | Results to skip. (2 means we start the response with the 3rd result) | int       | 0             |
| poster     | Filter to show only one user's tweets.                               | string    | -             |
| from       | Results posted after the given UNIX Timestamp.                       | int       | -             |

Returns a list containing JSON objects.

Example output:
```
[
    {
        "content": "No, I am your Father!",
        "id": 1,
        "poster": "Dart Vader",
        "timestamp": 330382800
    },
    {
        "content": "NoooOoOoOoooo!",
        "id": 2,
        "poster": "Luke",
        "timestamp": 330382820
    }
]
```


### /tweet POST
posting tweets: `/tweet` (method: POST)
expected request body:

```
{
    "content": "Do. Or do not. There is no try.",
    "poster": "Yoda"
}
```

The id and timestamp is managed by the server method.
The server only saves the first 20 character of the **poster** and the first 140 character of the **content**. It also has a basic protection against [SQL injections](https://en.wikipedia.org/wiki/SQL_injection) .

Returns the freshly saved data as a JSON object.

Example output:
```
{
    "content": "Do. Or do not. There is no try.",
    "id": 3,
    "poster": "Yoda",
    "timestamp": 330383020
}
```

## Client

The client is responsible to represent the previously saved tweets and to collect new ones from the user.

### Expected behavior

The client should be a console application running until the user enters "exit" or presses Ctrl+D.
It should run in a loop, and with every running it should perform the following:

1. Query tweets from the server
1. Format and print the previous tweets. Example: `Chewbacca <1977-05-25 20:16:10>: Uuuuuuurr Ahhhhrrr Uhrrr`
1. Ask the user for message input. (also allow refreshing the list and exiting)

Also handle all possible exceptions, even Ctrl+D exiting the application.

### Extra

If you managed to finish with the client to **match the excepted behaviour**, you can extend it with a better interface.
There are several ways to improve this basic terminal interface:

- You can write a UI with curses, where the messages are refreshing themselves, while the user enters the message
- You can use Tkinter, PyGame, Kivy or any other library or framework to create a great UI
- Also you could try a Flask and web based client, where the client is also a webserver.

If you try to create this extra version, please still keep the "basic" terminal based one you created first!
