// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Test du pipeline CI/CD GitHub Actions EL MEHDI

contract StudentRegistry {
    // Structure pour représenter un étudiant
    struct Student {
        string firstName;
        string lastName;
    }

    // Tableau dynamique stocké sur la blockchain
    Student[] public students;

    // Événement pour notifier l'interface lors d'un ajout
    event StudentRegistered(string firstName, string lastName);

    // 1. Fonction pour enregistrer un étudiant
    function addStudent(string memory _firstName, string memory _lastName) public {
        students.push(Student(_firstName, _lastName));
        emit StudentRegistered(_firstName, _lastName);
    }

    // 2. Fonction pour récupérer la liste complète de tous les étudiants
    function getAllStudents() public view returns (Student[] memory) {
        return students;
    }

    // 3. Fonction pour récupérer un étudiant spécifique par son ID (son index)
    function getStudentById(uint256 _index) public view returns (string memory firstName, string memory lastName) {
        require(_index < students.length, "Etudiant introuvable : ID invalide.");
        Student memory s = students[_index];
        return (s.firstName, s.lastName);
    }

    // 4. Fonction pour obtenir le nombre total d'étudiants
    function getStudentsCount() public view returns (uint256) {
        return students.length;
    }
}