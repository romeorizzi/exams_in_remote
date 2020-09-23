Configuare il file di settings in cui si specifica nell'unico tag presente la path del file .csv che indica gli studenti iscritti.

Il file .csv avrà questa struttura:

	VR000000;<PATH>;
	...
	VR999999;<PATH>;

Per ogni riga è specificato nella prima colonna la matricola a cui si fa riferimento, nella seconda colonna il percorso della cartella
in cui si trovano i file consegnati dal studente (i file dei video e il file VR000000_output.csv che contiene gli hash consegnati dallo studente).
E' importante che nelle varie cartelle segnalate non vi siano altri files al di fuori di quelli sopra citati.