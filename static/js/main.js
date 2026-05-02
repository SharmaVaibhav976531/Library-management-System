document.addEventListener('DOMContentLoaded', function() {
    console.log('LMS Frontend Initialized');
    document.querySelectorAll('table tr').forEach(row => {
        row.addEventListener('mouseover', () => row.style.backgroundColor = '#e9ecef');
        row.addEventListener('mouseout', () => row.style.backgroundColor = '');
    });
});