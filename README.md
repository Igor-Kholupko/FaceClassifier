# FaceClassifire
Web-Program for classifying massive of folders with photos on server by specific rules. Below is a description of these rules:
<br>
	<p>1. normal - one person shows on all photos in the folder. Folder are classified as good;
	<p>2. nonperson - the folder contains photos without peoples. Folder are classified as bad with "Nonperson" mark;
	<p>3. multiple - the folder contains photos of different peoples, and there no majority of one person photos. Folder are classified as bad with "Multiple" mark;
	<p>4. extra - the folder contains photos of many peoples, but photos of one person prevails over others. Photos of that person are classified as good, another - as bad in clone folder with "Extra" mark;
	<p>5. blurry - the folder contains one ore more blurred photos. Folder are classified as bad with "Blurry" mark;
	<p>6. label - the folder contains photos of one person but on some of photos present another people and "main" person face aren't most big. In this case such photos are classified as bad in clone folder with "Label" mark, another photos as good.
</br>
