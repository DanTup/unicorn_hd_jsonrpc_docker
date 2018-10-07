# DanTup / unicorn_hd_jsonrpc

A Docker container that exposes the Unicorn HD Hat library for Raspberry Pi over JSON-RPC WebSocket so that it can easily be controlled from other devices on your LAN and using any programming language.

```
docker run -p=8050:8050 --device=/dev/spidev0.0 dantup/unicorn_hd_jsonrpc
```

The port can be customised by passing `-p PORT` to the command:

```
PORT=8051; docker run -p=$PORT:$PORT --device=/dev/spidev0.0 dantup/unicorn_hd_jsonrpc -p $PORT
```

You can see help on other arguments (such as setting default rotation and whether to turn the screen off when quitting) with `-h`:

```
docker run dantup/unicorn_hd_jsonrpc -h
```

Once running, use a JSON-RPC library for your favourite language to control the Unicorn HD Hat. An example using Dart is shown below.

```dart
import 'dart:async';

import "package:json_rpc_2/json_rpc_2.dart" as json_rpc;
import 'package:json_rpc_2/json_rpc_2.dart';
import "package:web_socket_channel/io.dart";
import 'package:web_socket_channel/status.dart' as status;

main() async {
  var socket = IOWebSocketChannel.connect('ws://localhost:8050');
  var client = new json_rpc.Client(socket.cast<String>());
  client.listen();

  for (var x = 0; x < 16; x++) {
    for (var y = 0; y < 16; y++) {
      if (x % 2 == 0 && y < 8 || x % 2 == 1 && y >= 8) {
        await send(client, "set_pixel", [x, y, 146, 66, 244]);
      } else {
        await send(client, "set_pixel", [x, y, 0, 255, 0]);
      }
    }
  }
  await send(client, "show");
  await sleep();

  await send(client, "set_rotation", [90]);
  await send(client, "show");
  await sleep();

  await send(client, "set_all", [146, 66, 244]);
  await send(client, "show");
  await sleep();

  await send(client, "set_all", [255, 255, 0]);
  await send(client, "show");
  await sleep();

  await send(client, "get_rotation");
  await send(client, "get_shape");
  await send(client, "noise");
  await sleep();

  await send(client, "noise");
  await sleep();

  await send(client, "clear");
  await sleep();

  await socket.sink.close(status.normalClosure);
}

Future<void> send(Client client, String method, [List<Object> args]) async {
  print("> $method $args");
  var result = await client.sendRequest(method, args);
  print("< $result");
}

Future<void> sleep() => new Future.delayed(new Duration(seconds: 2));
```
