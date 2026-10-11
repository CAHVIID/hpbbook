# Airflow background sources

Source documents and measured data behind the airflow work in the book (room CFD appendix, window draught).

| File | What it is |
|---|---|
| `nielsen-1990-annex20-2d-test-case.pdf` | P. V. Nielsen (1990), *Specification of a two-dimensional test case*, IEA Annex 20 Research Item 1.45, Aalborg University, ISSN 0902-7513 R9040. Geometry and boundary conditions of the isothermal 2D room test (case 2D1). |
| `nielsen-1990-annex20-2d-measurements.xls` | The laser-Doppler measurements from the report: mean and rms u/U0 at x = H, x = 2H, y = h/2 and y = H − h/2, Re = 5000. |
| `nielsen-1990-annex20-2d-measurements.csv` | The same mean values converted for the room CFD code: `profile, coord, u_over_U0`, with y measured **up from the floor** and x/H along the room. |
| `bugenings-2025-louvre-element-report.pdf` | L. A. Bugenings, A. Kamari, L. Rong (2025), *Experimental Investigations of a Full-Scale Louvre Element: Methodology description and result presentation*, Aarhus University. |
| `bugenings-2025-louvre-element-dataset.zip` | The measured dataset for that report (velocity, temperature and flow meter logs, 3/5/7 ACH, with and without heat source), Zenodo, doi:10.5281/zenodo.14614814, CC BY 4.0. |
| `fitzner-finke-2012-baua-f2072-window-ventilation.pdf` | K. Fitzner, U. Finke (2012), *Lüftungsregeln für freie Lüftung*, BAuA research project F 2072, ISBN 978-3-88261-105-2. Field study of bottom-hung (tilt) window ventilation in an 80 m² office in winter. |

Note on the Annex 20 data: in the report (Fig. 1) y points **down from the ceiling**, so in the spreadsheet the column
labelled `y=h/2` is the wall jet under the ceiling and `y=H-h/2` is the flow near the floor. The spreadsheet's
coordinate header `y=x/H` means y/H for the vertical profiles and x/H for the horizontal ones.
