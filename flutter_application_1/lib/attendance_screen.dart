
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AttendanceScreen extends StatelessWidget {
  const AttendanceScreen({super.key});

  Future<void> markAttendance(String classId) async {
    final user = FirebaseAuth.instance.currentUser;
    await FirebaseFirestore.instance.collection('attendance').add({
      'studentId': user!.uid,
      'classId': classId,
      'date': DateTime.now(),
      'status': 'present'
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Attendance')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => markAttendance('class101'),
          child: const Text('Mark Attendance for Class 101'),
        ),
      ),
    );
  }
}