
package org.rcmd.apachejena_ptgl;

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
import org.apache.jena.vocabulary.VCARD;

public class CreateRdfResource {

    public static void main(String[] args) {

        System.out.println("=== Apache Jena Playground Startup ===");

        Model model = ModelFactory.createDefaultModel();
        Resource author = CreateRdfResource.createAuthor(model);
        CreateRdfResource.printModelStatements(model);

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

}
