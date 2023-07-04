This code has been a huge success and lays the actual fundamentals for the development of the GIBT algorithm. The code yields desired results. It's a moment to celebrate.
But along the results comes problems. In this version, the problems are less about the data and more about the performance. 
1) There is a significant time delay between the initiation of the code and its conclusion
2) AbeBooks data scrapping is still inaccurate in some instances

Both problems are dealable. It would require more efforts in optimization and developing "preference scrapping".

1) Optimization would require to use multiprocessing and multithreading to be used parallally along with overcoming the multiprocessing's problem of --name-- == '--main--'
2) "Preference Scrapping" would require would developing such functions which would enable scrapping on a preferential order. It would allow us to use multiple tags/elements to scrap data. This gives a fail-safe backup method. In case one the website doesn't contain the first element tag (as in the provided argument), it would use the 'second' element tag to scrap data. Same goes for 'second', 'third' and so on depending on the number of element tags we have provided in the argument
3) Instead of relying on element by element scrapping, multithreading would be leverage to scrap the entire data all at once

Analysing the data would open us upto new problems and possible solutions alongside.

I feel happy about this draft and aim to further development of the GIBT algorithm 

😊😊