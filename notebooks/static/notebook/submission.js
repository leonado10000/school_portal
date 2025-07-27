document.addEventListener('DOMContentLoaded', () => {
  const tableBody = document.getElementById('submissionTableBody');
  const sampleStudents = [
    { roll: 1, name: 'Alice', subject: 'Math' },
    { roll: 2, name: 'Bob', subject: 'Science' },
    { roll: 3, name: 'Charlie', subject: 'History' },
    { roll: 4, name: 'David', subject: 'Geography' },
    { roll: 5, name: 'Eva', subject: 'English' }
  ];

  sampleStudents.forEach(student => {
    const row = document.createElement('tr');

    const today = () => new Date().toISOString().split('T')[0];

    row.innerHTML = `
      <td>${student.roll}</td>
      <td>${student.name}</td>
      <td>${student.subject}</td>
      <td><input type="checkbox" class="check-btn" /></td>
      <td><input type="checkbox" class="incomplete-btn" /></td>
      <td class="check-date">-</td>
      <td class="incomplete-date">-</td>
    `;

    const checkBtn = row.querySelector('.check-btn');
    const checkDate = row.querySelector('.check-date');
    checkBtn.addEventListener('change', () => {
      checkDate.textContent = checkBtn.checked ? today() : '-';
    });

    const incompleteBtn = row.querySelector('.incomplete-btn');
    const incompleteDate = row.querySelector('.incomplete-date');
    incompleteBtn.addEventListener('change', () => {
      incompleteDate.textContent = incompleteBtn.checked ? today() : '-';
    });

    tableBody.appendChild(row);
  });
});
