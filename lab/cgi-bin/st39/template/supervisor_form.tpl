<form action="/cgi-bin/lab3.py">
    <input type="hidden" name = "student" value={1} />
    <input type="hidden" name = "id" value={2} />
    <input type="hidden" name = "action" value="save_supervisor" />
    Name: <input type="text" value="{3}" name="name"><br>
    Position: <input type="text" value="{4}" name="position"><br>
    Salary: <input type="text" value="{5}" name="salary"><br>
    Liberties: <input type="text" value="{6}" name="liberties"><br>
    Responsibility: <input type="text" value="{7}" name="responsibility"><br>


    <input type="submit" value="Save"/><br>
    <a href="{0}?student={1}"> <--- </a><br>

</form>