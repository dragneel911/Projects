document.addEventListener('DOMContentLoaded', () => {
    const studentForm = document.getElementById('student-form');
    const studentList = document.getElementById('student-list');
    const studentId = document.getElementById('student-id');
    const submitButton = document.getElementById('submit-button');

    // Guard against missing DOM elements to avoid runtime errors
    if (!studentForm || !studentList || !studentId || !submitButton) {
        console.warn('Student UI elements not found. Skipping script initialization.');
        return;
    }

    const API_URL = '/api/students'; 

    
    async function fetchStudents() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Network response was not ok');
            const students = await response.json();

            studentList.innerHTML = ''; 
            students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.id}</td>
                    <td>${student.first_name}</td>
                    <td>${student.last_name}</td>
                    <td>${student.email}</td>
                    <td>${student.major ?? ''}</td>
                    <td>
                        <button class="edit-btn" data-id="${student.id}">Edit</button>
                        <button class="delete-btn" data-id="${student.id}">Delete</button>
                    </td>
                `;
                studentList.appendChild(row);
            });
        } catch (error) {
            console.error('Failed to fetch students:', error);
        }
    }

    
    studentForm.addEventListener('submit', async (e) => {
        e.preventDefault(); //

        const id = studentId.value; 
        const studentData = {
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value,
            email: document.getElementById('email').value,
            major: document.getElementById('major').value,
        };

        let url = API_URL;
        let method = 'POST';

        
        if (id) {
            url = `${API_URL}/${id}`;
            method = 'PUT';
        }

        try {
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData),
            });

            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.error || 'Failed to save student');
            }

            resetForm();
            fetchStudents(); 
        } catch (error) {
            console.error('Error saving student:', error);
        }
    });

    
    studentList.addEventListener('click', async (e) => {
        
        if (e.target.classList.contains('delete-btn')) {
            const id = e.target.dataset.id;
            if (!confirm('Are you sure you want to delete this student?')) return;

            try {
                const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
                if (!response.ok) throw new Error('Failed to delete student');
                fetchStudents(); 
            } catch (error) {
                console.error('Error deleting student:', error);
            }
        }

        
        if (e.target.classList.contains('edit-btn')) {
            const id = e.target.dataset.id;
            const row = e.target.closest('tr');
            const cells = row.children;

            studentId.value = id; 
            document.getElementById('first_name').value = cells[1].textContent;
            document.getElementById('last_name').value = cells[2].textContent;
            document.getElementById('email').value = cells[3].textContent;
            document.getElementById('major').value = cells[4].textContent;

            submitButton.textContent = 'Update Student'; 
            window.scrollTo(0, 0);
        }
    });

  
    function resetForm() {
        studentForm.reset();
        studentId.value = ''; 
        submitButton.textContent = 'Add Student';
    }

    fetchStudents();
});