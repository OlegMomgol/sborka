import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Редактор профиля',
      theme: ThemeData(primarySwatch: const Color.fromARGB(255, 13, 139, 243)),
      home: const ProfileScreen(),
    );
  }
}

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  String name = 'Иришка';
  String status = 'Бездарь';

  Future<void> _editProfile() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => EditProfileScreen(currentName: name, currentStatus: status),
      ),
    );

    if (result != null && mounted) {
      setState(() {
        name = result['name'];
        status = result['status'];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Профиль')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const CircleAvatar(
              radius: 50,
              child: Icon(Icons.person, size: 60),
            ),
            const SizedBox(height: 20),
            Text('Имя: $name', style: const TextStyle(fontSize: 22)),
            const SizedBox(height: 10),
            Text('Статус: $status', style: const TextStyle(fontSize: 18, color: Color.fromARGB(255, 255, 254, 254))),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              onPressed: _editProfile,
              icon: const Icon(Icons.edit),
              label: const Text('Редактировать'),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 50)),
            ),
          ],
        ),
      ),
    );
  }
}

class EditProfileScreen extends StatefulWidget {
  final String currentName;
  final String currentStatus;

  const EditProfileScreen({super.key, required this.currentName, required this.currentStatus});

  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  late TextEditingController nameController;
  late TextEditingController statusController;

  @override
  void initState() {
    super.initState();
    nameController = TextEditingController(text: widget.currentName);
    statusController = TextEditingController(text: widget.currentStatus);
  }

  @override
  void dispose() {
    nameController.dispose();
    statusController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Редактировать профиль')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(labelText: 'Имя', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: statusController,
              decoration: const InputDecoration(labelText: 'Статус', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              onPressed: () {
                final updatedData = {
                  'name': nameController.text.trim(),
                  'status': statusController.text.trim(),
                };
                Navigator.pop(context, updatedData);
              },
              icon: const Icon(Icons.save),
              label: const Text('Сохранить'),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 50)),
            ),
          ],
        ),
      ),
    );
  }
}
