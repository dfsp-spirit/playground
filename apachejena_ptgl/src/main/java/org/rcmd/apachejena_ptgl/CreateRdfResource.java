
package org.rcmd.apachejena_ptgl;

import java.io.InputStream;

/**
 * This roughly follows the Apache Jena RDF API tutorial, see https://jena.apache.org/tutorials/rdf_api.html
 */
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.Statement;
import org.apache.jena.rdf.model.StmtIterator;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.vocabulary.VCARD;
import org.apache.jena.riot.Lang;

public class CreateRdfResource {

    public static void main(String[] args) {

        System.out.println("=== Apache Jena Playground Startup ===");

        Model model = ModelFactory.createDefaultModel();
        Resource author = CreateRdfResource.createAuthor(model);
        
        String authName = author.getProperty(VCARD.FN).toString();
        System.out.println("**Author name from main: " + authName);

        System.out.println("**Model Statements:");
        CreateRdfResource.printModelStatements(model);

        // print the full model string using default writer (rather dumb but fast, does NOT preserver blank nodes)
        System.out.println("**Full Model String (default writer):");
        model.write(System.out);

        // now write the model in a pretty form (but slow for very large models, preserves blank nodes)
        System.out.println("**Full Model String (pretty writer):");
        RDFDataMgr.write(System.out, model, Lang.RDFXML);

        // now write the model in N-triples format (fast, preserves blank nodes)
        System.out.println("**Full Model String (in NTRIPLES format):");
        RDFDataMgr.write(System.out, model, Lang.NTRIPLES);

        // Read a model file on disk
        Model myVcard = readModelFile("foaf.rdf", "http://example.org/test23/");
        RDFDataMgr.write(System.out, myVcard, Lang.NTRIPLES);

        System.out.println("=== Apache Jena Playground Exiting. ===");
    }

    public static Resource createAuthor(Model model) {
        // some definitions
        final String personURI = "http://somewhere/JohnSmith";
        final String givenName = "John";
        final String familyName = "Smith";
        final String fullName = givenName + " " + familyName;

        // create the resource
        Resource johnSmith = model.createResource(personURI);

        // add the property
        johnSmith.addProperty(VCARD.FN, fullName);
        johnSmith.addProperty(VCARD.Given, givenName);
        johnSmith.addProperty(VCARD.Family, familyName);

        return johnSmith;
    }

    public static void printModelStatements(Model model) {
        // list the statements in the Model
        StmtIterator iter = model.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt = iter.nextStatement(); // get next statement
            Resource subject = stmt.getSubject(); // get the subject
            Property predicate = stmt.getPredicate(); // get the predicate
            RDFNode object = stmt.getObject(); // get the object

            System.out.print(subject.toString());
            System.out.print(" " + predicate.toString() + " ");
            if (object instanceof Resource) {
                System.out.print(object.toString());
            }
            else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }

            System.out.println(" .");
        }
    }

    /**
     * 
     * @param inputFileName
     * @param localUrlPrefix Prefix added to local URLs. Can be NULL if and only if there are no local URLs in the document.
     * @return
     */
    public static Model readModelFile(String inputFileName, String localUrlPrefix) {
        // create an empty model
        Model model = ModelFactory.createDefaultModel();

        // use the RDFDataMgr to find the input file
        InputStream in = RDFDataMgr.open( inputFileName );
        if (in == null) {
            throw new IllegalArgumentException("File: " + inputFileName + " not found");
        }

        // read the RDF/XML file
        model.read(in, localUrlPrefix);

        return model;    
    }

}
